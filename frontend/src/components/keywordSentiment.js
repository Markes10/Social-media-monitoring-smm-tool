import React, { useState } from "react";
import { fetchKeywordAnalysis } from "../api";
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from "recharts";
import { Box, TextField, Button, Typography } from "@mui/material";

const COLORS = ["#4CAF50", "#F44336", "#FFC107"];

const KeywordSentiment = () => {
    const [keyword, setKeyword] = useState("");
    const [data, setData] = useState([]);

    const handleAnalyze = () => {
        fetchKeywordAnalysis(keyword).then((result) => {
            setData([
                { name: "Positive", value: result.Positive },
                { name: "Negative", value: result.Negative },
                { name: "Neutral", value: result.Neutral },
            ]);
        });
    };

    return (
        <Box sx={{ mt: 3 }}>
            <Typography variant="h6">Keyword Sentiment Analysis</Typography>
            <TextField
                label="Enter Keyword"
                variant="outlined"
                size="small"
                value={keyword}
                onChange={(e) => setKeyword(e.target.value)}
                sx={{ mr: 2 }}
            />
            <Button variant="contained" onClick={handleAnalyze}>
                Analyze
            </Button>

            {data.length > 0 && (
                <ResponsiveContainer width="100%" height={300}>
                    <PieChart>
                        <Pie data={data} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={100}>
                            {data.map((entry, index) => (
                                <Cell key={index} fill={COLORS[index]} />
                            ))}
                        </Pie>
                        <Tooltip />
                        <Legend />
                    </PieChart>
                </ResponsiveContainer>
            )}
        </Box>
    );
};

export default KeywordSentiment;
