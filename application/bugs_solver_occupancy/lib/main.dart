import 'package:flutter/material.dart';
import 'pages/welcome_screen.dart';

void main() => runApp(const App());

class App extends StatelessWidget {
  const App({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'MobileAppBugsSolver',
      theme: ThemeData(
        useMaterial3: true,
        colorSchemeSeed: const Color(0xFF222831), // background_colour
        scaffoldBackgroundColor: const Color(0xFF222831),
      ),
      home: const WelcomeScreen(),
    );
  }
}
