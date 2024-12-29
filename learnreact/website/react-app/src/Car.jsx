import  {useState} from 'react';

function Car(){
    const [car, setCar] = useState( {year:2024,
                                    make:"Ford",
                                    model:"Mustang"});
    function handleYearChange(e){
        // setCar(c=>({...c, year: e.target.value}))
        setCar({...car, year: e.target.value})
    };

    function handleMakeChange(e){
        // setCar(c=>({...c, make: e.target.value}))
        setCar({...car, make: e.target.value})
    };

    function handleModelChange(e){
        // setCar(c=>({...c, model: e.target.value}))
        setCar({...car, model: e.target.value})
    };

    return (
        <div>
        <p>My favourite car is: {car.year} {car.make} {car.model}</p> 
        <div> <label>Year: </label>       
            <input type="number" value={car.year} onChange={handleYearChange}/>
        </div>
        <div> <label>Make: </label>      
            <input type="text" value={car.make} onChange={handleMakeChange}/>
        </div>
        <div><label>Model: </label> 
            <input type="text" value={car.model} onChange={handleModelChange}/>
        </div>
        </div>  
    )
}
export default Car;