function Profilepicture() {
    const imageUrl = "./src/assets/flower.png";
    const handleClick = (e) =>e.target.style.display = "none";
  return (
    <img onClick={(e) =>handleClick(e)} src={imageUrl} alt="profile picture" />
  );
}
export default Profilepicture;