import { Link, useMatch, useResolvedPath } from "react-router-dom"
import homeIcon from './images/home_2413074.png';
import disasterTypesIcon from './images/storm_3095219.png';
import preparednessTipsIcon from './images/sticky-note_17576095.png';
export default function Navbar() {
  return (
    <nav className="nav">
      <Link to="/" className="site-title">
        Disaster Management
      </Link>
      <ul>
      <CustomLink to="/Home">
          <img src={homeIcon} alt="Home" className="icon" title="home" /> {/* Home icon */}
        </CustomLink>
        <CustomLink to="/DisasterTypes">
          <img src={disasterTypesIcon} alt="Disaster Types" className="icon" title="Disaster Types" /> {/* Disaster Types icon */}
        </CustomLink>
        <CustomLink to="/PreparednessTips">
          <img src={preparednessTipsIcon} alt="Preparedness Tips" className="icon" title="Prepardness tips"/> {/* Preparedness Tips icon */}
        </CustomLink>
        <button className="oli">Organisation Login</button>
      </ul>
    </nav>
  )
}

function CustomLink({ to, children, ...props }) {
  const resolvedPath = useResolvedPath(to)
  const isActive = useMatch({ path: resolvedPath.pathname, end: true })

  return (
    <li className={isActive ? "active" : ""}>
      <Link to={to} {...props}>
        {children}
      </Link>
    </li>
  )
}