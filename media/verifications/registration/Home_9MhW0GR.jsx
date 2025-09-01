import ellipse from "../../img/ellipse.png"
import { Slider } from "./slider/Slider"
import { Latest_Exchanges } from "./larest_exchanges/Latest_Exchanges"
import { Review } from "../review/Review"
import { Wallet } from "./wallet/Wallet"
import { Header } from "../header/Header"
import { Video } from "./video/videobg"
import { News } from "../news/News"
import { AcardionBlock } from "./acardion/Faq"
import Exchenger from "./exchanger/Exchenger"

const iconss =[
    "https://38dce7f7.naka-7nv.pages.dev/ApeCoin_3D.svg",
    "https://38dce7f7.naka-7nv.pages.dev/Avalanche_3D.svg",
    "https://38dce7f7.naka-7nv.pages.dev/Bitcoin_3D.svg",
    "https://38dce7f7.naka-7nv.pages.dev/EOS_3D.svg",
    "https://38dce7f7.naka-7nv.pages.dev/Ethereum_3D.svg",
    "https://38dce7f7.naka-7nv.pages.dev/Polygon_3D.svg",
    "https://38dce7f7.naka-7nv.pages.dev/Shiba Inu_3D 1.svg",
    "https://38dce7f7.naka-7nv.pages.dev/Solana_3D.svg",
    "https://38dce7f7.naka-7nv.pages.dev/USD Coin_3D.svg",
    ]



export const Home = ()=>{

    return(
        <>
        <div className="bggradient">
            <div className="icons_absolute">
            <div className='icons_home'>
                {iconss.map((el,index)=>(
                    <img className="icon_icon" key={index} src={el} alt="" />
                ))}
            </div>
            </div>
            <Header/>
            <img src={ellipse} className="absolutebg"/>
            <Exchenger/>
            <Slider/>
        </div>
        <Latest_Exchanges/>
        <Review/>
        <Wallet/>
        <Video/>
        <News/>
        <AcardionBlock/>
        </>
    )
}