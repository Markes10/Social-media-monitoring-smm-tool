import React, { useState } from "react";
import { View, Button, Text, WebView } from "react-native";
import axios from "axios";

const ReportsScreen = () => {
  const [reportUrl, setReportUrl] = useState("");

  const generateReport = async () => {
    try {
      const response = await axios.get("http://your-api-url/generate_report");
      setReportUrl(response.data.report_url);
    } catch (error) {
      console.error("Error generating report:", error);
    }
  };

  return (
    <View>
      <Button title="Generate Report" onPress={generateReport} />
      {reportUrl ? (
        <WebView source={{ uri: reportUrl }} style={{ height: 500, width: "100%" }} />
      ) : (
        <Text>Press the button to generate a report</Text>
      )}
    </View>
  );
};

export default ReportsScreen;
