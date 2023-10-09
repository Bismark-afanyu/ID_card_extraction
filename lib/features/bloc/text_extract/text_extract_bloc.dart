import 'package:bloc/bloc.dart';
import 'package:meta/meta.dart';

part 'text_extract_event.dart';
part 'text_extract_state.dart';

class TextExtractBloc extends Bloc<TextExtractEvent, TextExtractState> {
  TextExtractBloc() : super(TextExtractInitial()) {
    on<TextExtractEvent>((event, emit) {
      // TODO: implement event handler
      // Still to be implemented
    });
  }
}
