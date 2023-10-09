import 'package:flutter/material.dart';

void imagePickerModel(BuildContext context, {VoidCallback? onCameraTap, VoidCallback? onGalleryTap}) {
  showModalBottomSheet(
      context: context,
      builder: (context) {
        return Container(
            padding: const EdgeInsets.all(20),
            height: 220,
            child: Column(
              children: [
                GestureDetector(
                  onTap: onCameraTap,
                  child: Card(
                    child: Container(
                        padding: const EdgeInsets.all(15),
                        decoration: BoxDecoration(
                            borderRadius: BorderRadius.circular(15),
                            color: Colors.grey),
                        alignment: Alignment.center,
                        child: const Text("Camera",
                            style: TextStyle(
                                fontWeight: FontWeight.bold, fontSize: 20))),
                  ),
                ),
                const SizedBox(height: 10),
                GestureDetector(
                  onTap: onGalleryTap,
                  child: Card(
                    child: Container(
                        padding: const EdgeInsets.all(15),
                        alignment: Alignment.center,
                        decoration: BoxDecoration(
                            borderRadius: BorderRadius.circular(15),
                            color: Colors.grey),
                        child: const Text("Gallery",
                            style: TextStyle(
                                fontWeight: FontWeight.bold, fontSize: 20))),
                  ),
                )
              ],
            ));
      });
}
