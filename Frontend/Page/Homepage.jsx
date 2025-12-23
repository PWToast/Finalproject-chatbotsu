import { useAuth } from "../service/Auth"
function Homepage() {
      useAuth()
      
  return (
    <>
        <h1>Hello Welcome!</h1>
    </>
  )
}

export default Homepage