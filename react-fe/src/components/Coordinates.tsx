


class Coordinates{
    lat:Number;
    lon:Number;
    constructor(lat:Number,lon:Number){
        this.lat = lat;
        this.lon = lon;
    }

    toStringCoordinates(){
        return [this.lat.toString(), this.lon.toString()];
    }

}

export default Coordinates;