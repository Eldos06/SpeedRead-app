 import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:speedread_app/screens/schulte_screen.dart';

const _digitKeys = {
  '0': LogicalKeyboardKey.digit0,
  '1': LogicalKeyboardKey.digit1,
  '2': LogicalKeyboardKey.digit2,
  '3': LogicalKeyboardKey.digit3,
  '4': LogicalKeyboardKey.digit4,
  '5': LogicalKeyboardKey.digit5,
  '6': LogicalKeyboardKey.digit6,
  '7': LogicalKeyboardKey.digit7,
  '8': LogicalKeyboardKey.digit8,
  '9': LogicalKeyboardKey.digit9,
};

Widget _buildApp() {
  return MaterialApp(
    home: Builder(
      builder: (context) => Scaffold(
        body: Center(
          child: ElevatedButton(
            onPressed: () => Navigator.of(context).push(MaterialPageRoute(builder: (_) => const SchulteScreen())),
            child: const Text('Open'),
          ),
        ),
      ),
    ),
  );
}

Future<void> _selectSize3x3(WidgetTester tester) async {
  await tester.tap(find.byType(DropdownButton<int>));
  await tester.pump(const Duration(milliseconds: 300));
  await tester.tap(find.text('3 × 3').last);
  await tester.pump(const Duration(milliseconds: 300));
  await Future<void>.delayed(const Duration(seconds: 2));
  await tester.pump();
}

Future<void> _typeNumber(WidgetTester tester, int n) async {
  for (final ch in '$n'.split('')) {
    await tester.sendKeyEvent(_digitKeys[ch]!);
    await tester.pump(const Duration(milliseconds: 50));
  }
}

void main() {
  testWidgets('typing mode: digits 1..9 advance and finish with results dialog', (tester) async {
    await tester.runAsync(() async {
      await tester.pumpWidget(_buildApp());
      await tester.tap(find.text('Open'));
      await tester.pump(const Duration(milliseconds: 300));
      await Future<void>.delayed(const Duration(seconds: 2));
      await tester.pump();

      expect(find.text('Ввод с клавиатуры'), findsOneWidget);

      await _selectSize3x3(tester);

      expect(find.text('Ищи'), findsOneWidget);
      expect(find.text('1'), findsWidgets);

      for (var n = 1; n <= 9; n++) {
        await _typeNumber(tester, n);
      }
      await tester.pump(const Duration(milliseconds: 800));

      expect(find.text('Готово! 🎉'), findsOneWidget);
      expect(find.textContaining('Ошибок: 0'), findsOneWidget);
    });
  });

  testWidgets('manual mode: Старт/Стоп buttons drive the timer and finish', (tester) async {
    await tester.runAsync(() async {
      await tester.pumpWidget(_buildApp());
      await tester.tap(find.text('Open'));
      await tester.pump(const Duration(milliseconds: 300));
      await Future<void>.delayed(const Duration(seconds: 2));
      await tester.pump();

      await tester.tap(find.text('Старт/Стоп'));
      await tester.pump(const Duration(milliseconds: 300));
      await Future<void>.delayed(const Duration(seconds: 2));
      await tester.pump();

      expect(find.text('Старт'), findsOneWidget);
      expect(find.text('Стоп'), findsNothing);

      await tester.tap(find.text('Старт'));
      await tester.pump(const Duration(milliseconds: 300));

      expect(find.text('Стоп'), findsOneWidget);

      await Future<void>.delayed(const Duration(seconds: 1));
      await tester.pump();

      await tester.tap(find.text('Стоп'));
      await tester.pump(const Duration(milliseconds: 500));

      expect(find.text('Готово! 🎉'), findsOneWidget);
      expect(find.textContaining('Ошибок'), findsNothing);
    });
  });

  testWidgets('auto-exit mode: leaving the screen shows results before popping', (tester) async {
    await tester.runAsync(() async {
      await tester.pumpWidget(_buildApp());
      await tester.tap(find.text('Open'));
      await tester.pump(const Duration(milliseconds: 300));
      await Future<void>.delayed(const Duration(seconds: 2));
      await tester.pump();

      await tester.tap(find.text('До выхода'));
      await tester.pump(const Duration(milliseconds: 300));
      await Future<void>.delayed(const Duration(seconds: 2));
      await tester.pump();

      await Future<void>.delayed(const Duration(seconds: 1));
      await tester.pump();

      await tester.tap(find.byTooltip('Back'));
      await tester.pump(const Duration(milliseconds: 500));

      expect(find.text('Готово! 🎉'), findsOneWidget);

      await tester.tap(find.text('Ок'));
      await tester.pump(const Duration(milliseconds: 500));

      expect(find.text('Open'), findsOneWidget);
      expect(find.text('Таблица Шульте'), findsNothing);
    });
  });
}
