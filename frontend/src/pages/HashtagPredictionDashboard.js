import React, { useState } from "react";
import { View, Text, TextInput, Button } from "react-native";
import axios from "axios";

const HashtagPredictionDashboard = () => {
    const [hashtag, setHashtag] = useState("");
    const [prediction, setPrediction] = useState(null);
    const [contentIdeas, setContentIdeas] = useState([]);

    const fetchPrediction = async () => {
        const res = await axios.get(`http://your-api-url/predict_hashtag/${hashtag}`);
        setPrediction(res.data);
    };

    const fetchContentIdeas = async () => {
        const res = await axios.get(`http://your-api-url/recommend_content`);
        setContentIdeas(res.data.content_ideas);
    };

    return (
        <View>
            <Text>🔮 Hashtag & Content Predictions</Text>
            <TextInput 
                placeholder="Enter Hashtag (e.g., #AI)" 
                value={hashtag} 
                onChangeText={setHashtag}
            />
            <Button title="Predict Engagement" onPress={fetchPrediction} />
            <Button title="Get Content Ideas" onPress={fetchContentIdeas} />

            {prediction && (
                <View>
                    <Text>📈 Predicted Posts: {prediction.predicted_posts}</Text>
                </View>
            )}

            {contentIdeas.length > 0 && (
                <View>
                    <Text>📝 Content Recommendations:</Text>
                    {contentIdeas.map((idea, index) => (
                        <Text key={index}>👉 {idea}</Text>
                    ))}
                </View>
            )}
        </View>
    );
};

export default HashtagPredictionDashboard;
