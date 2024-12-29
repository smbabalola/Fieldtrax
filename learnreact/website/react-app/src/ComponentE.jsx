import React, {useState, useEffect, useRef} from 'react';

function ComponentE() {

  // let [number, setNumber] = useState(0);
  const ref = useRef(0);

  useEffect(() => {
    console.log("Component Rendered!")
  });
  
  function handleClick(){
    ref.current += 1; 
    console.log(ref.current);
  }

  return (
    <button onClick={handleClick}>Click me!</button>
  );
}
export default ComponentE;