import PropTypes from "prop-types";
function List(props){

    const category = props.category;
    const itemList = props.items;
    const listitems = itemList.map((item, index) => 
    <li key={index}>{
        item.name}: &nbsp; <b>{item.calories}</b></li>);
    return (<h3 className='list-category'>{category}
            <ol className='list-item'>{listitems}</ol>
            </h3>);
            
}
List.propTypes = { 
    items: PropTypes.arrayOf(
        PropTypes.shape(
        {id: PropTypes.number, 
        name: PropTypes.string, 
        calories: PropTypes.number})),
    category: PropTypes.string
};
List.defaultProps = {
    items: [],
    category: 'category'
};

export default List;