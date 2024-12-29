import { useState } from "react";
function Food() {
  //   const food1 = "Pizza";
  //   const food2 = "Burger";
  //   const food3 = "Pasta";

  // return (
  //   <ul>
  //       <li>i like {food1}</li>
  //       <li>i like {food2}</li>
  //       <li>i like {food3.toUpperCase()}</li>
  //   </ul>
  // )
  const [foods, setFoods] = useState(["Pizza", "Burger", "Pasta"]);

  function handleAddFood() {
    const foodInput = document.getElementById("foodInput");
    setFoods(f=>[...f, foodInput.value]);
  }

  function handleRemoveFood(index) {
    setFoods(foods.filter((_,i)=> i!==index));
  }

  return (
    <div>
      <h1>List of Foods</h1>
      <ul>
        {foods.map((food, index) => (
          <li key={index} onClick={()=>handleRemoveFood(index)}>{food}</li>
        ))}
      </ul>
      <input type="text" id="foodInput" placeholder="Enter Food name"/>
      <button onClick={handleAddFood}>Add Food</button>
      <button onClick={handleRemoveFood}>Remove Food</button>
    </div>
  );
}
export default Food;