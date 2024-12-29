import React, {useState, useEffect, useRef} from 'react';

function Stopwatch() {
    
  // let [number, setNumber] = useState(0);
  const ref = useRef(0);
  const intervalIdRef = useRef(null);
  const startTimeRef = useRef(0);
  const [time, setTime] = useState(0);
  const [running, setRunning] = useState(false);

  useEffect(() => {
    if(running){
      intervalIdRef.current = setInterval(() => {
        setTime(Date.now() - startTimeRef.current);
      }, 10);
      return () => clearInterval(intervalIdRef.current );
    }
  }, [running]);

  function handleStart(){
    setRunning(true);
    startTimeRef.current = Date.now() - time;
  }

  function handleStop(){
    setRunning(false);

  }

  function handleReset(){
    setTime(0);
    setRunning(false);
  }

  function formatTime(){
    let minutes = Math.floor(time / (1000*60) % 60).toString().padStart(2, '0');
    let seconds = Math.floor((time / 1000) % 60).toString().padStart(2, '0');
    let milliseconds = Math.floor((time % 1000) /10).toString().padStart(2, '0');
    return `${minutes}:${seconds}:${milliseconds}`;
  }

  return (
    <div className="stopwatch">
      <h1 className="display">{formatTime()}</h1>
      <div className="controls">
        <button className="start-button" onClick={handleStart}>Start</button>
        <button className="stop-button" onClick={handleStop}>Stop</button>
        <button className="reset-button" onClick={handleReset}>Reset</button>
      </div>
    </div>
  );
}
export default Stopwatch;