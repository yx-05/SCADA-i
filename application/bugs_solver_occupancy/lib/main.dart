import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'pages/welcome_screen.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized(); // ✅ ensure bindings before runApp
  runApp(const App());
}

class App extends StatelessWidget {
  const App({super.key});

  @override
  Widget build(BuildContext context) {
    return ScreenUtilInit(
      // ✅ Use a realistic design base — matches most Figma / modern devices
      designSize: const Size(430, 932), // e.g., Pixel 7 Pro / large iPhone base
      minTextAdapt: true,
      splitScreenMode: true,
      builder: (_, __) => MaterialApp(
        title: 'MobileAppBugsSolver',
        debugShowCheckedModeBanner: false,
        theme: ThemeData(
          useMaterial3: true,
          colorSchemeSeed: const Color(0xFF222831),
          scaffoldBackgroundColor: const Color(0xFF222831),
        ),
        home: const WelcomeScreen(), // 👈 your first screen
      ),
    );
  }
}
