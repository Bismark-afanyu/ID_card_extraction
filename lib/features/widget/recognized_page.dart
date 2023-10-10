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
  List<Face> _faces = [];

  @override
  void initState() {
    super.initState();
    final InputImage inputImage = InputImage.fromFilePath(widget.path!);
    processImage(inputImage);
  }

  @override
  Widget build(BuildContext context) {
    final int height = MediaQuery.of(context).size.height.toInt();
    return Container(
      child: Scaffold(
          appBar: AppBar(
            title: const Text("Text"),
          ),
          body: _isBusy
              ? const Center(child: CircularProgressIndicator())
              : SingleChildScrollView(
                  child: Expanded(
                      // padding: const EdgeInsets.all(20),
                      child: Column(
                        children: [
                          Container(
                            height: 100,
                            child: TextFormField(
                              controller: _controller,
                              maxLines: height,
                              decoration: const InputDecoration(
                                  hintText: "Text goes here..."),
                            ),
                          ),
                          Stack(
  
                            children: [
                              Positioned(
                                child: Container(
                                  decoration: BoxDecoration(
                                    image: DecorationImage(
                                        image: AssetImage(widget.path!),
                                        fit: BoxFit.cover
                                        ),
                                  )),
                              )
                              
                              // for (Face face in _faces)
                              //   _drawFaceRect(face, context),
                            ],
                          ),
                        ],
                      )),
                )),
    );
  }

  Widget _drawFaceRect(Face face, BuildContext context) {
    final rect = face.boundingBox;
    final paint = Paint()
      ..color = Colors.red
      ..strokeWidth = 2.0;

    return CustomPaint(
      painter: _FacePainter(rect, paint),
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

    _controller.text = recognizedText.text;

    /// End Busy state
    setState(() {
      _faces = faces;
      _isBusy = false;
    });
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
    return rect != oldDelegate.rect || paint != oldDelegate.paint;
  }
}
