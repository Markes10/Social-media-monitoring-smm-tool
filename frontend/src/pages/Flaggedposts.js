const approvePost = async (postId) => {
    await axios.post(`http://your-ec2-ip:8000/approve-post/${postId}`);
    alert("Post approved!");
};
