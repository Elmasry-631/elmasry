import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:get_it/get_it.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'core/theme/app_colors.dart';
import 'app/router.dart';

//lib/main.dart
final GetIt sl = GetIt.instance;

Future<void> _setupLocator() async {
  final prefs = await SharedPreferences.getInstance();
  sl.registerSingleton<SharedPreferences>(prefs);
  sl.registerSingleton<AppState>(AppState(prefs));
}

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  SystemChrome.setPreferredOrientations([DeviceOrientation.portraitUp]);
  SystemChrome.setSystemUIOverlayStyle(const SystemUiOverlayStyle(
    statusBarColor: Colors.transparent,
    statusBarIconBrightness: Brightness.light,
  ));
  await _setupLocator();
  runApp(const OdooSalesmanApp());
}

class OdooSalesmanApp extends StatelessWidget {
  const OdooSalesmanApp({super.key});

  @override
  Widget build(BuildContext context) {
    final appState = sl<AppState>();
    return AnimatedBuilder(
      animation: appState,
      builder: (_, __) => MaterialApp.router(
        title: 'Odoo Salesman',
        debugShowCheckedModeBanner: false,
        theme: ThemeData(
          useMaterial3: true,
          colorScheme: AppColors.scheme,
          scaffoldBackgroundColor: AppColors.navyDeep,
          cardColor: AppColors.navyMid,
          appBarTheme: const AppBarTheme(
            backgroundColor: AppColors.navyDeep,
            foregroundColor: AppColors.textPrimary,
            elevation: 0,
            centerTitle: false,
          ),
          navigationBarTheme: NavigationBarThemeData(
            backgroundColor: AppColors.navyMid,
            indicatorColor: AppColors.amber.withOpacity(0.25),
            labelTextStyle: WidgetStateProperty.all(
              const TextStyle(color: AppColors.textSecondary, fontSize: 11),
            ),
          ),
          elevatedButtonTheme: ElevatedButtonThemeData(
            style: ElevatedButton.styleFrom(
              backgroundColor: AppColors.amber,
              foregroundColor: AppColors.navyDeep,
              minimumSize: const Size.fromHeight(52),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
              textStyle: const TextStyle(fontWeight: FontWeight.w700, fontSize: 16),
            ),
          ),
          textTheme: const TextTheme(
            headlineLarge: TextStyle(color: AppColors.textPrimary, fontWeight: FontWeight.w800),
            headlineMedium: TextStyle(color: AppColors.textPrimary, fontWeight: FontWeight.w700),
            titleLarge: TextStyle(color: AppColors.textPrimary, fontWeight: FontWeight.w600),
            bodyLarge: TextStyle(color: AppColors.textPrimary),
            bodyMedium: TextStyle(color: AppColors.textSecondary),
          ),
        ),
        routerConfig: buildRouter(appState),
      ),
    );
  }
}