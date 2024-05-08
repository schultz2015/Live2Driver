var app;
var flaging=0
var backPIC=0
var emotion
var EMOLIST= ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
var ModelAdress
var Settings={}
// PixiJS
const {
	Application,
	live2d: { Live2DModel }
} = PIXI;

// Kalidokit
const {
	Face,
	Vector: { lerp },
	Utils: { clamp }
} = Kalidokit;


// 1, Live2D指定

const videoElement = document.getElementById("my-video");
const guideCanvas = document.getElementById("my-guides");
const emoElement = document.getElementById("my-emo");
//document.getElementByClassName("but").addEventListener("click",Motion())
let currentModel, facemesh, preparemodel;
main()
document.getElementById("reload").addEventListener("click", function() {
	main()
});

// 处理开始
async function main() {
	modelAdress()
	const modelUrl = "./assets/"+ModelAdress
	getModel(ModelAdress)

	// 2, PixiJS设定
	app = new PIXI.Application({
		view: document.getElementById("my-live2d"),
		autoStart: true,
		backgroundAlpha: 0,
		transparent:true,
		backgroundColor: 0x000000,
		resizeTo: window
	});

		// 3, Live2D载入
	preparemodel = await Live2DModel.from(modelUrl, { autoInteract: false });
	currentModel = await Live2DModel.from(modelUrl, { autoInteract: false });

	preparemodel.scale.set(0.4);
	currentModel.scale.set(0.4);

	preparemodel.interactive = true;
	currentModel.interactive = true;

	preparemodel.anchor.set(0.5, 0.5);
	currentModel.anchor.set(0.5, 0.5);

	preparemodel.position.set(window.innerWidth * 0.5, window.innerHeight * 0.8);
	currentModel.position.set(window.innerWidth * 0.5, window.innerHeight * 0.8);
	// 4, Live2D鼠标移动
	currentModel.on("pointerdown", e => {
		currentModel.offsetX = e.data.global.x - currentModel.position.x;
		currentModel.offsetY = e.data.global.y - currentModel.position.y;
		currentModel.dragging = true;
		preparemodel.offsetX = e.data.global.x - preparemodel.position.x;
		preparemodel.offsetY = e.data.global.y - preparemodel.position.y;
		preparemodel.dragging = true;
	});
	preparemodel.on("pointerdown", e => {
		currentModel.offsetX = e.data.global.x - currentModel.position.x;
		currentModel.offsetY = e.data.global.y - currentModel.position.y;
		currentModel.dragging = true;
		preparemodel.offsetX = e.data.global.x - preparemodel.position.x;
		preparemodel.offsetY = e.data.global.y - preparemodel.position.y;
		preparemodel.dragging = true;
	});
	currentModel.on("pointerup", e => {
		currentModel.dragging = false;
		preparemodel.dragging = false;
	});
	preparemodel.on("pointerup", e => {
		currentModel.dragging = false;
		preparemodel.dragging = false;
	});
	currentModel.on("pointermove", e => {
		if (currentModel.dragging) {
			currentModel.position.set(
				e.data.global.x - currentModel.offsetX,
				e.data.global.y - currentModel.offsetY
			);
		}
		if (preparemodel.dragging) {
			preparemodel.position.set(
				e.data.global.x - preparemodel.offsetX,
				e.data.global.y - preparemodel.offsetY
			);
		}
	});
	preparemodel.on("pointermove", e => {
		if (currentModel.dragging) {
			currentModel.position.set(
				e.data.global.x - currentModel.offsetX,
				e.data.global.y - currentModel.offsetY
			);
		}
		if (preparemodel.dragging) {
			preparemodel.position.set(
				e.data.global.x - preparemodel.offsetX,
				e.data.global.y - preparemodel.offsetY
			);
		}
	});


//	// 4, 
//	preparemodel.on("pointerdown", e => {
//		preparemodel.offsetX = e.data.global.x - preparemodel.position.x;
//		preparemodel.offsetY = e.data.global.y - preparemodel.position.y;
//		preparemodel.dragging = true;
//		// console.log(35.53521728515625 -165.7662109375001)
//	});
//	preparemodel.on("pointerup", e => {
//		preparemodel.dragging = false;
//		var updateFn = preparemodel.internalModel.motionManager.update;
//    	var coreModel = preparemodel.internalModel.preparemodel;
//	});
//	preparemodel.on("pointermove", e => {
//		if (preparemodel.dragging) {
//			preparemodel.position.set(
//				e.data.global.x - preparemodel.offsetX,
//				e.data.global.y - preparemodel.offsetY
//			);
//		}
//	});
	// 5, Live2D缩放
	document.querySelector("#my-live2d").addEventListener("wheel", e => {
		e.preventDefault();
		currentModel.scale.set(
			clamp(currentModel.scale.x + event.deltaY * -0.001, -0.5, 10)
		);
		preparemodel.scale.set(
			clamp(preparemodel.scale.x + event.deltaY * -0.001, -0.5, 10)
		);
	});

	// 6, Live2D加入
	app.stage.addChild(currentModel);

	// 7, mediapipe
	facemesh = new FaceMesh({
		locateFile: file => {
			return `https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh/${file}`;
		}
	});
	facemesh.setOptions({
		maxNumFaces: 1,
		refineLandmarks: true,
		minDetectionConfidence: 0.5,
		minTrackingConfidence: 0.5
	});
	facemesh.onResults(onResults);

	// 8, Web摄像头
	startCamera();

}

// emption传参
function back(dataUrl){
    backPIC+=1
    if(backPIC==25){
        console.log(backPIC)
        backPIC=0
        po(dataUrl)
        console.log(emotion)
        var detect=EMOLIST.indexOf(emotion)
        if(detect>=0){
            emoElement.innerHTML=emotion
			if (Settings['allow']==="yes") {
				action(detect)
			}       
        }

    }

//   setTimeout(console.log(1),1000)
}

function action(number){
	flaging=number
	app.stage.removeChild(currentModel)
	app.stage.addChild(preparemodel)
	if(flaging==6){
		app.stage.removeChild(preparemodel)
		app.stage.addChild(currentModel)
	}
	if(flaging==0){
        preparemodel.internalModel.motionManager.startMotion(Settings['Angry'].split(":")[0],Settings['Angry'].split(":")[1],2);
	}
	if(flaging==1){
        preparemodel.internalModel.motionManager.startMotion(Settings['Disgust'].split(":")[0],Settings['Disgust'].split(":")[1],2);
	}
	if(flaging==2){
        preparemodel.internalModel.motionManager.startMotion(Settings['Fear'].split(":")[0],Settings['Fear'].split(":")[1],2);
	}
	if(flaging==3){
        preparemodel.internalModel.motionManager.startMotion(Settings['Happy'].split(":")[0],Settings['Happy'].split(":")[1],2);
	}
	if(flaging==4){
        preparemodel.internalModel.motionManager.startMotion(Settings['Sad'].split(":")[0],Settings['Sad'].split(":")[1],2);
	}
	if(flaging==5){
        preparemodel.internalModel.motionManager.startMotion(Settings['Surprise'].split(":")[0],Settings['Surprise'].split(":")[1],2);
}
}

const onResults = results => {
	// 9, mediapipe描绘人脸
	drawResults(results.multiFaceLandmarks[0]);
	// 10, Live2D图层传参
	animateLive2DModel(results.multiFaceLandmarks[0]);

    const videoDom = document.getElementById("my-video");
    const currentTime=videoDom.currentTime
    const canvas=document.createElement('canvas')
    canvas.width=videoDom.clientWidth
    canvas.height=videoDom.clientHeight
    canvas.getContext('2d').drawImage(videoDom,0,0,canvas.width,canvas.height)
    const dataUrl=canvas.toDataURL('image/png').replace("data:image/png;base64,","")// 转base64
    back(dataUrl)



};

const drawResults = points => {
	if (!guideCanvas || !videoElement || !points) return;
	guideCanvas.width = videoElement.videoWidth;
	guideCanvas.height = videoElement.videoHeight;
	let canvasCtx = guideCanvas.getContext("2d");
	canvasCtx.save();
	canvasCtx.clearRect(0, 0, guideCanvas.width, guideCanvas.height);
	drawConnectors(canvasCtx, points, FACEMESH_TESSELATION, {
		color: "#C0C0C070",
		lineWidth: 1
	});
	if (points && points.length === 478) {
		drawLandmarks(canvasCtx, [points[468], points[468 + 5]], {
			color: "#ffe603",
			lineWidth: 2
		});
	}
};

// 面部数据解析
const animateLive2DModel = points => {
	if(!currentModel || !points) return;
	let riggedFace = Face.solve(points, {
		runtime: "mediapipe",
		video: videoElement
	});
	rigFace(riggedFace, 0.7); // 0.7为插值系数 
};

const rigFace = (result, lerpAmount = 0.7) => {
	if (!currentModel || !result) return;
	const updateFn = currentModel.internalModel.motionManager.update;
	const coreModel = currentModel.internalModel.coreModel;

	currentModel.internalModel.motionManager.update = (...args) => {
		currentModel.internalModel.eyeBlink = undefined;

		coreModel.setParameterValueById(
			"ParamEyeBallX",
			lerp(
				result.pupil.x,
				coreModel.getParameterValueById("ParamEyeBallX"),
				lerpAmount
			)
		);
		coreModel.setParameterValueById(
			"ParamEyeBallY",
			lerp(
				result.pupil.y,
				coreModel.getParameterValueById("ParamEyeBallY"),
				lerpAmount
			)
		);

		coreModel.setParameterValueById(
			"ParamAngleX",
			lerp(
				result.head.degrees.y,
				coreModel.getParameterValueById("ParamAngleX"),
				lerpAmount
			)
		);
		coreModel.setParameterValueById(
			"ParamAngleY",
			lerp(
				result.head.degrees.x,
				coreModel.getParameterValueById("ParamAngleY"),
				lerpAmount
			)
		);
		coreModel.setParameterValueById(
			"ParamAngleZ",
			lerp(
				result.head.degrees.z,
				coreModel.getParameterValueById("ParamAngleZ"),
				lerpAmount
			)
		);

		const dampener = 0.3;
		coreModel.setParameterValueById(
			"ParamBodyAngleX",
			lerp(
				result.head.degrees.y * dampener,
				coreModel.getParameterValueById("ParamBodyAngleX"),
				lerpAmount
			)
		);
		coreModel.setParameterValueById(
			"ParamBodyAngleY",
			lerp(
				result.head.degrees.x * dampener,
				coreModel.getParameterValueById("ParamBodyAngleY"),
				lerpAmount
			)
		);
		coreModel.setParameterValueById(
			"ParamBodyAngleZ",
			lerp(
				result.head.degrees.z * dampener,
				coreModel.getParameterValueById("ParamBodyAngleZ"),
				lerpAmount
			)
		);

		let stabilizedEyes = Kalidokit.Face.stabilizeBlink(
			{
				l: lerp(
					result.eye.l,
					coreModel.getParameterValueById("ParamEyeLOpen"),
					0.7
				),
				r: lerp(
					result.eye.r,
					coreModel.getParameterValueById("ParamEyeROpen"),
					0.7
				)
			},
			result.head.y
		);

		coreModel.setParameterValueById("ParamEyeLOpen", stabilizedEyes.l);
		coreModel.setParameterValueById("ParamEyeROpen", stabilizedEyes.r);
		coreModel.setParameterValueById(
			"ParamMouthOpenY", 
			lerp(result.mouth.y, coreModel.getParameterValueById("ParamMouthOpenY"), 0.3)
		);
		coreModel.setParameterValueById(
			"ParamMouthForm",
			0.3 + lerp(result.mouth.x, coreModel.getParameterValueById("ParamMouthForm"), 0.3)
		);
	};
};

// Web摄像头
const startCamera = ()=>{
	const camera = new Camera(videoElement, {
		onFrame: async ()=>{
			await facemesh.send({ image: videoElement });
			
		},
		width: 640, height: 480
	});
	camera.start();
};

function modelAdress(){
	$.ajax({
        url: '/api/address',
        method: "POST",
		async:false,
		contentType: "application/json;charset=utf-8",
        success:function(data){
//            alert("请求已经提交.");
//             console.log(data.responseText)
             ModelAdress=data
			 console.log(ModelAdress)
			 
        },error:function(data){
//             alert("There Is Error！");
//             console.log(data.responseText)
			ModelAdress=data['modelAddresss']
        }

    });
}

function getModel(modelUrl){
    $.ajax({
        url: '/api/model',
        method: "POST",
		contentType: "application/json;charset=utf-8",
        dataType:"json",
        data:JSON.stringify({"model":modelUrl}),
        success:function(data){
//            alert("请求已经提交.");
//             console.log(data.responseText)
             Settings=data['settings']
			 console.log(Settings)
			 console.log(Settings['Angry'].split(":")[0])
        },error:function(data){
//             alert("There Is Error！");
//             console.log(data.responseText)
             Settings=data['settings']
        }

    });
}
function po(dataUrl){
    $.ajax({
        url: '/api/data',
        method: "POST",
        dataType:"json",
        data:{proid:dataUrl},
        success:function(data){
//            alert("请求已经提交.");
//             console.log(data.responseText)
             emotion=data.responseText
        },error:function(data){
//             alert("There Is Error！");
//             console.log(data.responseText)
             emotion=data.responseText
        }

    });
//        .done(function(e){
//           alert('done!');
//        });
}

