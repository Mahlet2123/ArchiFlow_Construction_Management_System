import axios from "axios";
import React from "react";


class App extends React.Component {
  state = { details: [], error: null }

  componentDidMount() {
    axios.get('http://localhost:5000/api/users/')
    .then((res) => {
      this.setState({
        details: res.data,
        error: null,
      });
    })
    .catch((error) => {
      console.error("Error fetching data:", error);
      this.setState({ error });
    });
  }

  render () {
    const { details, error } = this.state;

    return (
      <div>
        <header>
          <h1>
            Data from django: Users Email    
          </h1>
        </header>
        <hr />
        {error ? (
          <div>Error fetching data. Please try again later.</div>
        ) : (
          details.map((output, id) => (
            <div key={id}>
              <h2>{output.email}</h2>
            </div>
          ))
        )}
      </div>
    );
  }
}

export default App
