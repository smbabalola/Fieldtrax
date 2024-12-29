// ToDoList.jsx
import { useState }  from 'react';

function ToDoList(){
    const [todos, setTodos] = useState(["Learn React", "Learn JSX", "Learn Hooks"]);
    const [todo, setTodo] = useState("");

    function handleAddTodo(){
        if (todo.trim() === "") return;
        setTodos(todos.concat(todo));
        setTodo("");
    }

    function handleRemove(index){
        setTodos(todos.filter((_,i)=> i!==index));
    }

    function handleChange(e){
        setTodo(e.target.value);
    }

    function moveUp(index){
        if(index === 0) return;
        const newTodos = [...todos];
        const temp = newTodos[index];
        newTodos[index] = newTodos[index-1];
        newTodos[index-1] = temp;
        setTodos(newTodos);
    }

    function moveDown(index){
        if(index === todos.length - 1) return;
        const newTodos = [...todos];
        const temp = newTodos[index];
        newTodos[index] = newTodos[index+1];
        newTodos[index+1] = temp;
        setTodos(newTodos);
    }

    return(
        <div>
            <h2>My Todo List</h2>
            <ul>
                {todos.map((todo, index)=>(
                    <li key={index} onDoubleClick={()=>handleRemove(index)}>{todo}  
                    <button className="moveUp-button" onClick={() =>moveUp(index)}> Up
                    </button>
                    <button className="moveDown-button" onClick={() =>moveDown(index)}> Down
                    </button>
                    </li>
                    
                ))}
            </ul>
            <input type="text" value={todo} onChange={handleChange} placeholder='Enter todo'/>
            <button onClick={handleAddTodo}>Add Todo</button>
        </div>
    )
}
export default ToDoList;