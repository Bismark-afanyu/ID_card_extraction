import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:newapp/features/utils/image_cropperView.dart';
import 'package:newapp/features/utils/image_picker.dart';
import 'package:newapp/features/utils/model_dialog.dart';
import 'package:newapp/features/widget/recognized_page.dart';

void main() {
  runApp(const MaterialApp(home: MyApp()));
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Text Extraction App")),
      body: Center(
          child: Padding(
              padding: const EdgeInsets.all(20.0),
              child: Column(
                children: [
                  Center(
                      child: Container(
                          margin: const EdgeInsets.only(top: 150.0),
                          child: const Text('TEXT EXTRACTION FROM IMAGE',
                              style: TextStyle(
                                  fontWeight: FontWeight.bold, fontSize: 20)))),
                  const SizedBox(
                    height: 100,
                  ),
                  Container(
                      child: const Center(
                    child: Text(
                        textAlign: TextAlign.center,
                        "This is a test app for text extraction from image to help implement our work better.",
                        style: TextStyle(fontSize: 16)),
                  ))
                ],
              ))),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () {
          imagePickerModel(context, onCameraTap: () {
            pickImage(ImageSource.camera).then((value) {
              if (value != '') {
                imageCropperView(value, context).then((value) {
                  if (value != '') {
                    Navigator.push(
                        context,
                        MaterialPageRoute(
                            builder: (_) => RecognizePage(path: value)));
                  }
                });
              }
            });
          }, onGalleryTap: () {
            pickImage(ImageSource.gallery).then((value) {
              if (value != '') {
                imageCropperView(value, context).then((value) {
                  if (value != '') {
                    imageCropperView(value, context).then((value) {
                      if (value != '') {
                        Navigator.push(
                            context,
                            MaterialPageRoute( 
                                builder: (_) => RecognizePage(path: value)));
                      }
                    });
                  }
                });
              }
            });
          });
        },
        label: const Text("Extract"),
        tooltip: "Fetch Photo",
      ),
    );
  }
}
