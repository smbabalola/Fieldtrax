
function Button() {
//   const styles = {
    
//     padding: "10px 20px",
//     backgroundColor: "blue",
//     color: "white",
//     border: "none",
//     borderRadius: "5px",
//     cursor: "pointer",
// }
// let count = 0;
// const handleClick = (name) => {
//   count++
//   if(count <= 5){
//     console.log(`${name} you clicked me ${count} times`);
// }
// else{
//   console.log(`${name} stop clicking me!`);
// }
// };

// const handleClick2 = (name) => {
//      console.log(`${name} stop clicking me`);
// };

const handleClick = (e) => e.target.textContent = "Danget!";

return (
  <button className="button" onDoubleClick={(e) => handleClick(e)}>
    Click me!
  </button>
);
}
export default Button;