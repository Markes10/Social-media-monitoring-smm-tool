const autoReply = async (postId) => {
    const response = await axios.post(`http://your-ec2-ip:8000/auto-reply/${postId}`);
    alert("AI Reply: " + response.data.auto_reply);
};
