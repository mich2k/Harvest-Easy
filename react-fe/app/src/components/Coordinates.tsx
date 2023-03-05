


class Coordinates{
    lat:number;
    lon:number;
    constructor(lat:number,lon:number){
        this.lat = lat;
        this.lon = lon;
    }

    toStringCoordinates(){
        return [this.lat.toString(), this.lon.toString()];
    }

}

export default Coordinates;