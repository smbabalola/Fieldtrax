import {useState, useEffect} from 'react';

function DigitalClock(){
    const [time, setTime] = useState(new Date());

    useEffect(()=>{
        const interval = setInterval(()=>{
            setTime(new Date());
        }, 1000);
        return () => clearInterval(interval);
    }, []);

    // function handleReset(){
    //     setTime(new Date().toLocaleTimeString());
    // }
    function padZero(number){
        return number < 10 ? '0' + number : number;
    }

    function formatTime(){  
        // const date = new Date();
        const hours = time.getHours().toString().padStart(2, '0');
        const minutes = time.getMinutes().toString().padStart(2, '0');
        const seconds = time.getSeconds().toString().padStart(2, '0');
        const meridiem = hours>=12? 'PM' : 'AM';
        return `${padZero(hours)}:${padZero(minutes)}:${padZero(seconds)}:${meridiem}`;
    }

    return(
        <div className= "clock-container">
            <h1 className='clock'>Time</h1>
            <span>{formatTime()}</span>
        </div>
    );


}
export default DigitalClock;