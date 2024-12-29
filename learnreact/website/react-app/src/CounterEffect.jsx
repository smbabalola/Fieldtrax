import {useState, useEffect} from 'react';

function CounterEffect(){ 
    // const [count, setCount] = useState(0);
    // const [message, setMessage] = useState("");
    // const [color, setColor] =  useState("black");
    
    // useEffect(()=>{
    //     if(count === 0){
    //         setMessage("Zero");
    //     } else if(count % 2 === 0){
    //         setMessage("Even");
    //     } else {
    //         setMessage("Odd");
    //     }
    // }, [count, color]);

    // function changeColor(){
    //     setColor(c => c === "black" ? "red" : "black");
    // }

    // return (
    //     <div>
    //         <h1>{count} is {message}</h1>
    //         <button onClick={()=>setCount(count + 1)}>Increment</button>
    //         <button onClick={()=>setCount(count - 1)}>Decrement</button>
    //         <button onClick={changeColor}>Change Color</button>
    //     </div>
    // );#

    const [width, setWidth] = useState(window.innerWidth);
    const [height, setHeight] = useState(window.innerHeight);
    useEffect(()=>{
        window.addEventListener('resize', handleResize);    
        console.log('event listener added');
        return () => {
            window.removeEventListener('resize', handleResize);
            console.log('event listener removed');
        }
    }, []);

    useEffect(()=>{
        document.title = `Size: ${width} x ${height}`;
    
    }, [width, height]);

    function handleResize(){
        setWidth(window.innerWidth);
        setHeight(window.innerHeight);
    }

    return(
        <div>
            <h1>Window Width: {width}</h1>
            <h1>Window Height: {height}</h1>
        </div>
    );  
}
export default CounterEffect;