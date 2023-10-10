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
                  _buildImageContainer(height),
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

  Widget _buildImageContainer(int height) {
    return Container(
      height: height / 2,
      child: Stack(
        children: [
          Image.file(File(inputImage.filePath!)),
          for (Face face in _faces) _drawFaceRect(face),
        ],
      ),
    );
  }

  Widget _drawFaceRect(Face face) {
    final rect = face.boundingBox;
    final paint = Paint()
      ..color = Colors.red
      ..strokeWidth = 2.0;

    return CustomPaint(
      painter: _FacePainter(rect, paint),
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
  final Rect rect;
  final Paint draw;

  _FacePainter(this.rect, this.draw);

  @override
  void paint(Canvas canvas, Size size) {
    canvas.drawRect(rect, draw);
  }

  @override
  bool shouldRepaint(_FacePainter oldDelegate) {
    return rect != oldDelegate.rect || draw != oldDelegate.draw;
  }
}
