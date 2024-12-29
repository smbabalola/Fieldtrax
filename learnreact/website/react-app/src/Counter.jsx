import React from 'react';

function Counter(){
    const [count, setCount] = React.useState(0);
    // const increment = () => setCount(count + 1);
    // const decrement = () => setCount(count - 1);
    const reset = () => setCount(0);

    function increment(){
        // setCount(count + 1);
        setCount(c => c + 1);
        setCount(c => c + 1);
        setCount(c => c + 1);
    } 

    function decrement(){
      // setCount(count + 1);
      setCount(c => c - 1);
      setCount(c => c - 1);
      setCount(c => c - 1);
  } 

    return (
      <div>
        <h1>{count}</h1>
        <button onClick={increment}>Increment</button>
        <button onClick={reset}>Reset</button>
        <button onClick={decrement}>Decrement</button>

      </div>
    );

}
export default Counter;