import './Announcement.css'
import Marquee from 'react-fast-marquee';

const Announcement=()=>{
    return(
        <div className="announcement">
            <Marquee>
            <div className="at text1">
            <span>news alert blah blah 1</span>
            <span>news alert blah blah 2</span>
            <span>news alert blah blah 3</span>
            <span>news alert blah blah 4</span>
            </div>
            </Marquee>
        </div>
        
    )

}
export default Announcement;