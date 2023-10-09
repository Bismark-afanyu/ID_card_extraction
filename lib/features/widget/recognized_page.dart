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
  @override
  void initState() {
    // TODO: implement initState
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
                  child: TextFormField(controller: _controller, maxLines: MediaQuery.of(context).size.height.toInt(),decoration: const InputDecoration(hintText: "Text goes here..."),))),
    );
  }

  void processImage(InputImage image) async {
    final textRecognizer = TextRecognizer(script: TextRecognitionScript.latin);
    setState(() {
      _isBusy = true;
    });
    final RecognizedText recognizedText =
        await textRecognizer.processImage(image);
        final options = FaceDetectorOptions();
final faceDetector = FaceDetector(options: options);
final List<Face> faces = await faceDetector.processImage(image);

    _controller.text = recognizedText.text;

    /// End Busy state
    setState(() {
      _isBusy = false;
    });
  }
}
