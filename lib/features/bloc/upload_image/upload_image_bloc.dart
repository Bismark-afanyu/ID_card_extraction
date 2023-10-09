import 'package:bloc/bloc.dart';
import 'package:meta/meta.dart';

part 'upload_image_event.dart';
part 'upload_image_state.dart';

class UploadImageBloc extends Bloc<UploadImageEvent, UploadImageState> {
  UploadImageBloc() : super(UploadImageInitial()) {
    on<UploadImageEvent>((event, emit) {
      // TODO: implement event handler
      _getImage();
    });
  }
}

_getImage(){
  
}