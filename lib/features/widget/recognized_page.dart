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
    // final double height = MediaQuery.of(context).size.height.toInt() / 2;
    return Container(
      child: Scaffold(
          appBar: AppBar(
            title: const Text("Text"),
          ),
          body: _isBusy
              ? const Center(child: CircularProgressIndicator())
              : SingleChildScrollView(
                  child: Container(
                      padding: const EdgeInsets.all(20),
                      child: Column(
                        children: [
                          TextFormField(
                            controller: _controller,
                            maxLines: 100,
                            decoration: const InputDecoration(
                                hintText: "Text goes here..."),
                          ),
                          FittedBox(
                            child: Stack(
                              children: [
                                Image.asset(widget.path!),
                              ],
                            ),
                          ),
                        ],
                      )),
                )),
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
    for (Face face in faces) {
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

  _drawFaceRect(List<Face> faces, BuildContext context) {
    for (Face face in faces) {
      final rect = face.boundingBox;
      final paint = Paint()
        ..color = Colors.red
        ..strokeWidth = 2.0;
      return CustomPaint(
        painter: FacePainter(faces),
      );
    }
  }
}

class FacePainter extends CustomPainter {
  final List<Face> faces;
  final List<Rect> rects = [];

  FacePainter(this.faces) {
    for (var i = 0; i < faces.length; i++) {
      rects.add(faces[i].boundingBox);
    }
  }

  @override
  void paint(Canvas canvas, Size size) {
    final Paint paint = Paint()
      ..style = PaintingStyle.stroke
      ..strokeWidth = 15.0
      ..color = Colors.blue;

    for (var i = 0; i < faces.length; i++) {
      canvas.drawRect(rects[i], paint);
    }
  }

  @override
  bool shouldRepaint(FacePainter oldDelegate) {
    return false;
  }
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