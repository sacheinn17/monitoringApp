import {dataBase} from "./api.js"

const db = new dataBase;

export function getDate(today = new Date){
    return today.getFullYear() + '-' + String(today.getMonth() + 1).padStart(2, '0') + '-' + String(today.getDate()).padStart(2, '0');}

export function getDates(date)
{
    let curr = new Date(date);
    console.log(date)
    let firstDayofWeek = curr.getDate() - curr.getDay();
    console.log(curr)
    let days = [];
    if (firstDayofWeek > -1){
        for (const x of Array(7).keys()){
            curr = new Date(date);
            days.push(getDate(new Date(curr.setDate(firstDayofWeek+x))))
            }
        }
    else
    {
        return ["null"];
    }
    return days;
}

export async function getCatTimeWithDate(database,dates)
{
    let dayWithCatogary = [];
    for (const x of Array(7).keys()){
        let t2 = await database.getCatogariesAndTime(dates[x]);
        if (t2[0] != null){
            dayWithCatogary.push(t2)
        }
        else{
            t2 = [{"time":0}]
            dayWithCatogary.push(t2[0])
        }
    }
    return dayWithCatogary
}

export async function getTimeByCat(date,catogary){
    let t = await db.getCatogariesAndTime(date);
    // console.log(date,t)
    if(t[0] !=null){
        for (const x of t){
            // console.log(x)
            if (x.name === catogary){
                return x.time;
            }
        }
    }
    else{
        return 0;
    }
}

export function getTimeCat(date,catogary)
{
    return db.getCatogariesAndTime(date).then(
        t =>{
            if(t[0] !=null){
                for (const x of t){
                    // console.log(x)
                    if (x.name === catogary){
                        // console.log(x);
                        return x.time/60;
                    }
                }
            }
            else{
                return 0;
                
            }
        }
    )
}