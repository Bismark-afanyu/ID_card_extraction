import 'package:flutter/material.dart';
import 'package:google_mlkit_face_detection/google_mlkit_face_detection.dart';
import 'package:google_mlkit_text_recognition/google_mlkit_text_recognition.dart';

class RecognizePage extends StatefulWidget {
  const RecognizePage({super.key, this.path});
  final String? path;

  @override
  State<RecognizePage> createState() => _RecognizePageState();
}

class _RecognizePageState extends State<RecognizePage> {
  bool _isBusy = false;
  final TextEditingController _controller = TextEditingController();
  final List<Face> _faces = [];

  @override
  void initState() {
    super.initState();
    final InputImage inputImage = InputImage.fromFilePath(widget.path!);
    processImage(inputImage);
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      child: Scaffold(
          appBar: AppBar(
            title: const Text("Text"),
          ),
          body: _isBusy
              ? const Center(child: CircularProgressIndicator())
              : Container(
                  padding: const EdgeInsets.all(20),
                  child: Column(
                    children: [
                      TextFormField(
                        controller: _controller,
                        maxLines: MediaQuery.of(context).size.height.toInt(),
                        decoration: const InputDecoration(
                            hintText: "Text goes here..."),
                      ),
                      Stack(
                        children: [
                          Container(
                            child: Image.asset(widget.path!),
                          ),
                        ],
                      ),
                    ],
                  ))),
    );
  }

  void processImage(InputImage image) async {
    final textRecognizer = TextRecognizer(script: TextRecognitionScript.latin);
    final options =
        FaceDetectorOptions(performanceMode: FaceDetectorMode.accurate);
    final faceDetector = FaceDetector(options: options);
    setState(() {
      _isBusy = true;
    });
    final RecognizedText recognizedText =
        await textRecognizer.processImage(image);
    final List<Face> faces = await faceDetector.processImage(image);
    for (Face face in faces){
      _faces.add(face);
    }

    _controller.text = recognizedText.text;
    // for (Face face in faces) {
    //   _drawFaceRect(face, context);
    // }

    /// End Busy state
    setState(() {
      _isBusy = false;
    });
  }

  // _drawFaceRect(Face face, BuildContext context) {
  //   final rect = face.boundingBox;
  //   final paint = Paint()
  //     ..color = Colors.red
  //     ..strokeWidth = 2.0;

  //   return CustomPaint(painter: MyPainter(),);
  // }
}

// class MyPainter extends CustomPainter {

//   @override
//   void paint(Canvas canvas, Size size) {
// canvas.drawRect(rect, paint)
//   }

//   @override
//   bool shouldRepaint(MyPainter oldDelegate) => false;

//   @override
//   bool shouldRebuildSemantics(MyPainter oldDelegate) => false;
// }