import {useState} from 'react'

function MyComponent() {
//     usestate hook
//     const [name, setName] = useState("Guest");
//     const [age, setAge] = useState(20);
//     const [isEmployed, setIsEmployed] = useState(false);
// //   return <h1>Hello World</h1>;
// const updateName = () => {
//     setName("Shola Babalola")
//     console.log(name)
// }

// const incrementAge = () => {
//     setAge(age+5)
//     console.log(age)
// }

// const changeStatus = () => {
//     setIsEmployed(!isEmployed)
//     console.log(isEmployed)
// }

// return (
//     <div>
//         <h1>My name is: {name}</h1>
//         <button onClick={updateName}>Set Name</button>
//         <h1>My age is: {age}</h1>
//         <button onClick={incrementAge}>Increment Age</button>
//         <h1>Employed: {isEmployed ? "Yes" : "No"}</h1>
//         <button onClick={changeStatus}>change Status</button>
//     </div>
// )
//usestate hook examples
    const [name, setName] = useState("Guest");
    const [quantity, setQuantity] = useState(20); 
    const [comment, setComment] = useState("");
    const [payment, setPayment] = useState("Cash");
    const [shipping, setShipping] = useState("Pickup")

    function handleNameChange(e) {
        setName(e.target.value)
    }

    function handleQuantityChange(e) {
        setQuantity(e.target.value)
    }
    function handleCommentChange(e) {
        setComment(e.target.value)
    }

    function handlePaymentChange(e) {
        setPayment(e.target.value)  
    }  

    function handleShippingChange(e) { 
        setShipping(e.target.value)
    }

    return (
        <>
        <div>
            <input type="text" value={name} onChange={(handleNameChange)}/>
            <h1>Your name is: {name}</h1>
        </div>
        <div>
            <input type="number" value={quantity} onChange={(handleQuantityChange)}/>
            <h1>Quantity: {quantity}</h1>   
        </div>
        <div>
            <textarea value={comment} onChange={(handleCommentChange)} 
            placeholder='enter delivery instructions'></textarea>
            <h1>Comment: {comment}</h1> 
        </div>
        <div>
            <select value={payment} onChange={(handlePaymentChange)}>
                <option value="">Select an option</option>
                <option value="Cash">Cash</option>
                <option value="Card">Card</option>
                <option value="Transfer">Transfer</option>
            </select>
            <h1>Payment: {payment}</h1>
        </div>
        <div>
            <input type="radio" value="Pickup" checked={shipping === "Pickup"} 
            onChange={handleShippingChange}/>Pickup
            <input type="radio" value="Delivery" checked={shipping === "Delivery"} 
            onChange={handleShippingChange}/>Delivery
            <h1>Shipping: {shipping}</h1>
        </div>
        </>
    )

}
export default MyComponent;