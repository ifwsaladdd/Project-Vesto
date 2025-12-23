import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;


void main() {
  runApp(const MicroInvestApp());
}

class MicroInvestApp extends StatelessWidget {
  const MicroInvestApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'MicroInvest',
      home: DashboardScreen(),
    );
  }
}

class DashboardScreen extends StatelessWidget {
Future<Map<String, dynamic>> fetchPortfolio() async {
  try {
    final response = await http
        .get(Uri.parse("http://10.0.2.2:5000/portfolio"))
        .timeout(const Duration(seconds: 5));

    if (response.statusCode != 200) {
      throw Exception("Server error ${response.statusCode}");
    }

    return jsonDecode(response.body);
  } catch (e) {
    print("ERROR FETCHING PORTFOLIO: $e");
    throw e;
  }
}


@override
Widget build(BuildContext context) {
  return Scaffold(
    appBar: AppBar(title: const Text("Dashboard")),
    body: FutureBuilder(
  future: fetchPortfolio(),
  builder: (context, snapshot) {
    if (!snapshot.hasData) {
      return const Center(child: CircularProgressIndicator());
    }

    final data = snapshot.data as Map<String, dynamic>;

    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Text("Total Invested: \$${data['total_invested']}"),
        Text("Portfolio Value: \$${data['portfolio_value']}"),
        Text("Nominal ROI: ${data['nominal_roi']}%"),
        Text("Real ROI: ${data['real_roi']}%"),
      ],
    );
    },
  ),
  );
}
}
