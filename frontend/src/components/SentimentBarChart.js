import React, { useEffect, useState } from "react";
import { fetchPosts } from "../api";
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from "recharts";
import { Box, Typography } from "@mui/material";

const SentimentBarChart = () => {
    const [chartData, setChartData] = useState([]);

    useEffect(() => {
        fetchPosts().then(posts => {
            const sentimentCounts = {};

            posts.forEach(post => {
                const key = post.platform;
                if (!sentimentCounts[key]) {
                    sentimentCounts[key] = { platform: key, Positive: 0, Negative: 0, Neutral: 0 };
                }
                sentimentCounts[key][post.sentiment]++;
            });

            setChartData(Object.values(sentimentCounts));
        });
    }, []);

    return (
        <Box sx={{ textAlign: "center", mt: 3 }}>
            <Typography variant="h6">Sentiment by Platform</Typography>
            <ResponsiveContainer width="100%" height={300}>
                <BarChart data={chartData}>
                    <XAxis dataKey="platform" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="Positive" fill="#4CAF50" />
                    <Bar dataKey="Negative" fill="#F44336" />
                    <Bar dataKey="Neutral" fill="#FFC107" />
                </BarChart>
            </ResponsiveContainer>
        </Box>
    );
};

export default SentimentBarChart;
