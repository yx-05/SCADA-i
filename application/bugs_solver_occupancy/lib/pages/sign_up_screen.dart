import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';

const _hint = Color(0xFFC4C4C4);
const _bg = Color(0xFF222831);
final fieldGap = SizedBox(height: 15.h);

class SignUpScreen extends StatefulWidget {
  const SignUpScreen({
    super.key,
    required this.onBack,
    required this.onGoToLogin,
  });

  final VoidCallback onBack;
  final VoidCallback onGoToLogin;

  @override
  State<SignUpScreen> createState() => _SignUpScreenState();
}

class _SignUpScreenState extends State<SignUpScreen> {
  final _formKey = GlobalKey<FormState>();
  final _fullName = TextEditingController();
  final _email = TextEditingController();
  final _password = TextEditingController();
  bool _rememberMe = false;

  @override
  void dispose() {
    _fullName.dispose();
    _email.dispose();
    _password.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      resizeToAvoidBottomInset: true,
      backgroundColor: Colors.white,
      body: SafeArea(
        top: false,
        child: Padding(
          padding: EdgeInsets.fromLTRB(16.w, 24.h, 16.w, 16.h),
          child: Form(
            key: _formKey,
            child: SingleChildScrollView(
              padding: EdgeInsets.only(bottom: 32.h),
              keyboardDismissBehavior: ScrollViewKeyboardDismissBehavior.onDrag,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  SizedBox(height: 8.h),
                  Text(
                    "Create Your Account Now !",
                    style: TextStyle(
                      fontSize: 22.sp,
                      fontWeight: FontWeight.w800,
                      color: Colors.black,
                    ),
                    textAlign: TextAlign.center,
                  ),
                  SizedBox(height: 10.h),
                  Text(
                    "The journey begins! Create your account to access and manage the university's hardware. Monitor devices, control systems, and track usage all from one dashboard.",
                    style: TextStyle(
                      fontSize: 12.sp,
                      color: Colors.black,
                    ),
                    textAlign: TextAlign.center,
                  ),
                  SizedBox(height: 16.h),

                  // Full name
                  TextFormField(
                    controller: _fullName,
                    style: TextStyle(fontSize: 15.sp),
                    decoration: InputDecoration(
                      labelText: 'Enter Full Name',
                      labelStyle: TextStyle(color: _hint, fontSize: 14.sp),
                      constraints: BoxConstraints(minHeight: 50.h),
                      contentPadding: EdgeInsets.symmetric(
                          vertical: 10.h, horizontal: 12.w),
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.all(Radius.circular(10.r)),
                        gapPadding: 4.w,
                      ),
                      errorStyle: TextStyle(
                          fontSize: 12.sp, height: 0.8, color: Colors.red),
                    ),
                    validator: (v) => (v == null || v.isEmpty) ? 'Required' : null,
                  ),
                  fieldGap,

                  // Email
                  TextFormField(
                    controller: _email,
                    style: TextStyle(fontSize: 15.sp),
                    decoration: InputDecoration(
                      labelText: 'Enter Email',
                      labelStyle: TextStyle(color: _hint, fontSize: 14.sp),
                      constraints: BoxConstraints(minHeight: 50.h),
                      contentPadding: EdgeInsets.symmetric(
                          vertical: 10.h, horizontal: 12.w),
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.all(Radius.circular(10.r)),
                        gapPadding: 4.w,
                      ),
                      errorStyle: TextStyle(
                          fontSize: 12.sp, height: 0.8, color: Colors.red),
                    ),
                    keyboardType: TextInputType.emailAddress,
                    validator: (v) {
                      if (v == null || v.isEmpty) return 'Required';
                      final re = RegExp(r'^[^@]+@[^@]+\.[^@]+$');
                      return re.hasMatch(v) ? null : 'Enter a valid email';
                    },
                  ),
                  fieldGap,

                  // Password
                  TextFormField(
                    controller: _password,
                    style: TextStyle(fontSize: 15.sp),
                    decoration: InputDecoration(
                      labelText: 'Enter Password',
                      labelStyle: TextStyle(color: _hint, fontSize: 14.sp),
                      constraints: BoxConstraints(minHeight: 50.h),
                      contentPadding: EdgeInsets.symmetric(
                          vertical: 10.h, horizontal: 12.w),
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.all(Radius.circular(10.r)),
                        gapPadding: 4.w,
                      ),
                      errorStyle: TextStyle(
                          fontSize: 12.sp, height: 0.8, color: Colors.red),
                    ),
                    obscureText: true,
                    validator: (v) =>
                    (v != null && v.length >= 6) ? null : 'Min 6 characters',
                  ),
                  SizedBox(height: 5.h),

                  Row(
                    children: [
                      Checkbox(
                        value: _rememberMe,
                        onChanged: (v) => setState(() => _rememberMe = v ?? false),
                        activeColor: Colors.black,
                      ),
                      Text('Remember me',
                          style: TextStyle(color: Colors.black, fontSize: 14.sp)),
                    ],
                  ),
                  SizedBox(height: 2.h),

                  // Get Started
                  SizedBox(
                    height: 48.h,
                    child: FilledButton(
                      style: FilledButton.styleFrom(
                        backgroundColor: const Color(0xFF222831),
                        foregroundColor: Colors.white,
                        side: BorderSide(color: _bg, width: 1.w),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(30.r),
                        ),
                      ),
                      onPressed: () {
                        if (_formKey.currentState!.validate()) {
                          ScaffoldMessenger.of(context).showSnackBar(
                            const SnackBar(content: Text('Account created!')),
                          );
                          widget.onBack();
                        } else {
                          setState(() {});
                        }
                      },
                      child: Text(
                        'Get Started',
                        style: TextStyle(fontSize: 16.sp, fontFamily: 'Inter'),
                      ),
                    ),
                  ),
                  SizedBox(height: 12.h),

                  // Back
                  SizedBox(
                    height: 48.h,
                    child: FilledButton(
                      style: FilledButton.styleFrom(
                        backgroundColor: const Color(0xFF222831),
                        foregroundColor: Colors.white,
                        side: BorderSide(color: Colors.black, width: 1.w),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(30.r),
                        ),
                      ),
                      onPressed: widget.onBack,
                      child: Text(
                        'Back',
                        style: TextStyle(fontSize: 16.sp, fontFamily: 'Inter'),
                      ),
                    ),
                  ),
                  SizedBox(height: 16.h),

                  // Divider
                  Row(
                    children: [
                      Expanded(
                          child:
                          Divider(thickness: 1.h, color: Colors.grey)),
                      Padding(
                        padding: EdgeInsets.symmetric(horizontal: 8.w),
                        child: Text(
                          "Sign up with",
                          style: TextStyle(color: Colors.grey, fontSize: 14.sp),
                        ),
                      ),
                      Expanded(
                          child:
                          Divider(thickness: 1.h, color: Colors.grey)),
                    ],
                  ),
                  SizedBox(height: 8.h),

                  // Social buttons
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      IconButton(
                        onPressed: () {},
                        icon: Image.asset(
                          'assets/facebook_icon.png',
                          height: 45.h,
                          errorBuilder: (_, __, ___) =>
                              Icon(Icons.facebook_outlined, size: 30.sp),
                        ),
                      ),
                      SizedBox(width: 24.w),
                      IconButton(
                        onPressed: () {},
                        icon: Image.asset(
                          'assets/google_icon.png',
                          height: 44.h,
                          errorBuilder: (_, __, ___) =>
                              Icon(Icons.g_mobiledata, size: 30.sp),
                        ),
                      ),
                    ],
                  ),
                  SizedBox(height: 8.h),

                  // Already have an account
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Text(
                        "Already have an account? ",
                        style:
                        TextStyle(color: Colors.black, fontSize: 14.sp),
                      ),
                      GestureDetector(
                        onTap: widget.onGoToLogin,
                        child: Text(
                          "Log In",
                          style: TextStyle(
                            color: Colors.blue,
                            fontSize: 14.sp,
                            fontWeight: FontWeight.bold,
                            decoration: TextDecoration.underline,
                          ),
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
