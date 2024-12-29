import {useState} from 'react';

function MyCar(){
    const [car, setCar] = useState([]);
    const [year, setYear] = useState(new Date().getFullYear());
    const [make, setMake] = useState("");
    const [model, setModel] = useState("");

    function handleAddCar(e){
        const newCar = {year: year, 
                        make: make, 
                        model: model};
        setCar(c =>[...c, newCar]);

        setYear(new Date().getFullYear());
        setMake("");
        setModel("");
    };

    function handleRemoveCar(index){
        setCar(car.filter((_,i)=> i!==index));
    };

    function handleYearChange(e){
        setYear(e.target.value);
    };

    function handleMakeChange(e){
        setMake(e.target.value);
    };
    
    function handleModelChange(e){  
        setModel(e.target.value);
    }

    return(
        <div>
            <h2>List of car Objects</h2>
            <ul>
                {car.map((car, index)=>(
                    <li key={index} onClick={()=>handleRemoveCar(index)}>{car.year} {car.make} {car.model}</li>
                ))}
            </ul>
            <input type="number" value={year} onChange={handleYearChange}/>
            <input type="text" value={make} onChange={handleMakeChange}
            placeholder='Enter car make'/>
            <input type="text" value={model} onChange={handleModelChange}
            placeholder='Enter car model'/>
            <button onClick={handleAddCar}>Add Car</button>
        </div>
    )
}

export default MyCar;