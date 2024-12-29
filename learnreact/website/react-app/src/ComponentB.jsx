import ComponentC from './ComponentC';

function ComponentB() {
  return (
    <div className = "box">
      <h1>ComponentB</h1>
      <h2></h2>
      <ComponentC />
    </div>
  );
}
export default ComponentB;