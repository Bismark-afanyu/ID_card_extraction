import 'dart:io';

import 'package:flutter/material.dart';
import 'package:google_mlkit_face_detection/google_mlkit_face_detection.dart';
import 'package:google_mlkit_text_recognition/google_mlkit_text_recognition.dart';

class RecognizePage extends StatefulWidget {
  const RecognizePage({Key? key, required this.path}) : super(key: key);

  final String path;

  @override
  _RecognizePageState createState() => _RecognizePageState();
}

class _RecognizePageState extends State<RecognizePage> {
  bool _isBusy = false;
  final TextEditingController _controller = TextEditingController();
  late InputImage inputImage;
  List<Face> _faces = [];

  @override
  void initState() {
    super.initState();
    inputImage = InputImage.fromFilePath(widget.path);
    _processImage(inputImage);
  }

  @override
  Widget build(BuildContext context) {
    final int height = MediaQuery.of(context).size.height.toInt();

    return Scaffold(
      appBar: AppBar(
        title: const Text("Text"),
      ),
      body: _isBusy
          ? const Center(child: CircularProgressIndicator())
          : SingleChildScrollView(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  _buildTextInputField(height),
                  _buildImageContainer(height, context, inputImage.filePath!),
                ],
              ),
            ),
    );
  }

  Widget _buildTextInputField(int height) {
    return Container(
      height: 100,
      child: TextFormField(
        controller: _controller,
        maxLines: height,
        decoration: const InputDecoration(
          hintText: "Text goes here...",
        ),
      ),
    );
  }

  Widget _buildImageContainer(int height, BuildContext context, String path) {
    return Container(
      height: height / 2,
      child: Stack(
        children: [
          Image.file(File(inputImage.filePath!)),
          Positioned(left: 0, top: 0,child: CustomPaint(painter: _FacePainter(_faces),))
          // for (Face face in _faces) _drawFaceRect(face, context, path),
        ],
      ),
    );
  }

  Widget _drawFaceRect(Face face, BuildContext context, String path) {
    final rect = face.boundingBox;
    print("Faces are here: ${rect}");
    // final paint = Paint()
    //   ..color = Colors.blue
    //   ..strokeWidth = 0.1;

    return Positioned(
      left: rect.left,right: rect.right,top: rect.top,bottom: rect.bottom,
      child: CustomPaint(
        // painter: _FacePainter(rect: rect, imagePath: path),
      ),
    );
  }

  Future<void> _processImage(InputImage? inputor) async {
    setState(() {
      _isBusy = true;
    });

    try {
      inputor = InputImage.fromFilePath(widget.path);
      final textRecognizer =
          TextRecognizer(script: TextRecognitionScript.latin);
      final options =
          FaceDetectorOptions(performanceMode: FaceDetectorMode.accurate);
      final faceDetector = FaceDetector(options: options);

      final RecognizedText recognizedText =
          await textRecognizer.processImage(inputor);
      final List<Face> faces = await faceDetector.processImage(inputor);

      _controller.text = recognizedText.text;

      setState(() {
        _faces = faces;
        _isBusy = false;
      });
    } catch (e) {
      // Handle any exceptions or errors here
      setState(() {
        _isBusy = false;
      });
      print('Error processing image: $e');
    }
  }
}

class _FacePainter extends CustomPainter {
  // final Rect rect;
  // final Paint draw;

  // _FacePainter(this.rect, this.draw);

  // @override
  // void paint(Canvas canvas, Size size) {
  //   canvas.drawRect(rect, draw);
  // }

  // @override
  // bool shouldRepaint(_FacePainter oldDelegate) {
  //   return rect != oldDelegate.rect || draw != oldDelegate.draw;
  // }

  // final Rect rect;
  // final String imagePath;

  // _FacePainter({required this.rect, required this.imagePath});

  // @override
  // void paint(Canvas canvas, Size size) {
  //   final draw = Paint()
  //     ..color = Colors.red
  //     ..style = PaintingStyle.stroke
  //     ..strokeWidth = 0.10;

  //   // final image = FileImage(File(imagePath));
  //   // image.resolve(ImageConfiguration()).addListener(
  //   //   ImageStreamListener((info, _) {
  //   //     final imageInfo = info.image;
  //   //     final width = size.width / imageInfo.width;
  //   //     final height = size.height / imageInfo.height;

  //       // final transformedRect = Rect.fromLTRB(
  //       //   rect.left * width,
  //       //   rect.top * height,
  //       //   rect.right * width,
  //       //   rect.bottom * height,
  //       // );
  //       canvas.drawRect(rect, draw);
  //     // }),
  //   // );
  // }

  @override
  bool shouldRepaint(_FacePainter oldDelegate) => false;
  _FacePainter(this.faces);
  final List<Face> faces;
  @override
  void paint(Canvas canvas, Size size) {
    final Paint paint1 = Paint()
      ..style = PaintingStyle.stroke
      ..strokeWidth = 1.0
      ..color = Colors.red;
    for (final Face face in faces) {
      final left = face.boundingBox.left;
      final top = face.boundingBox.top;
      final right = face.boundingBox.right;
      final bottom = face.boundingBox.bottom;

      canvas.drawRect(Rect.fromLTRB(left, top, right, bottom), paint1);
      // void paintContour(FaceContourType type) {
      //   final contour = face.contours[type];
      //   if (contour?.points != null){
      //     for (final Point point in contour!.points){
      //       canvas.drawCircle(Offset(dx, dy))
      //     }
      //   }
      // }
    }
    // @override
    // bool shouldRepaint(F oldDelegate) {
    //   return oldDelegate.imageSize != imageSize || oldDelegate.faces != faces;
    // }
  }
}
// }
