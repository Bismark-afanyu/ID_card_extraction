import 'package:image_picker/image_picker.dart';

Future<String> pickImage(ImageSource source) async {
  final ImagePicker picker = ImagePicker();

  String path = '';
  final getImage = await picker.pickImage(source: source);
  if (getImage != null) {
    path = getImage.path;
  } else {
    path = '';
  }
  return path;
}
