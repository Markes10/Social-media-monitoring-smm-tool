import React, { useState } from "react";
import { View, TextInput, Button, Text } from "react-native";
import axios from "axios";

const AlertsScreen = () => {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");

  const subscribeToAlerts = async () => {
    try {
      const response = await axios.post("http://your-api-url/subscribe_alerts", { email });
      setMessage(response.data.message);
    } catch (error) {
      console.error("Error subscribing to alerts:", error);
      setMessage("Subscription failed.");
    }
  };

  return (
    <View>
      <Text>Enter your email to receive trend alerts:</Text>
      <TextInput 
        placeholder="Enter email" 
        value={email} 
        onChangeText={setEmail} 
        style={{ borderWidth: 1, padding: 8, marginBottom: 10 }} 
      />
      <Button title="Subscribe" onPress={subscribeToAlerts} />
      {message ? <Text>{message}</Text> : null}
    </View>
  );
};

export default AlertsScreen;
