# DEPRECATED
# DEPRECATED
# DEPRECATED
# DEPRECATED
# DEPRECATED
echo "! DEPRECATED !"
echo ""
echo ""



echo "This script will download the OSM extract of regione Emilia-Romagna or Modena province"
echo "If you use this script upgrade from PBF_URL TO PBF_PATH !"
echo "Will also set-up the .osm.pbf file for docker-compose"

echo ""

OSM_EXTRACT_PATH="$HOME/nominatim/osm_extract/"
OSM_EXTRACT_NAME="er.osn.pbf"
#OSM_EXTRACT_DOWNLOAD_URL="https://gmichele.it/er.osm.pbf"
OSM_EXTRACT_DOWNLOAD_URL="https://gmichele.it/modena.osm.pbf"

OSM_MD5="1ef9b08e9b0f1fad6e41d63e71e2a8ae"

while true; do
    read -p "Do you wish to proceed? " yn
    case $yn in
        [Yy]* )
            mkdir -p $OSM_EXTRACT_PATH
            cd $OSM_EXTRACT_PATH
            if [ -e $OSM_EXTRACT_NAME  ];then
                md5=($(md5sum $OSM_EXTRACT_NAME))
                if [ $md5 != $OSM_MD5 ]; then
                    echo "!!!"
                    echo "Your local database extract IS CORRUPTED, re-downloading.."
                    echo "!!!"

                    rm $OSM_EXTRACT_PATH$OSM_EXTRACT_NAME
                    wget -P $OSM_EXTRACT_PATH -O $OSM_EXTRACT_NAME "$OSM_EXTRACT_DOWNLOAD_URL";
                else
                    echo ""
                    echo "Appears you already have the database extract installed, and is NOT corrupted"
                    echo "The download will be skipped"
                    echo "-----"
                    echo "original md5: $OSM_MD5"
                    echo "your installed extract md5: $md5"
                    echo "-----"

                fi
            else
                echo "Your do not have a local database extract, downloading.."

                wget -P $OSM_EXTRACT_PATH -O $OSM_EXTRACT_NAME "$OSM_EXTRACT_DOWNLOAD_URL";
            fi
            echo "OK!"
            
            while true; do
                read -p "Do you wish to run docker-compose, (note it will take some time on first execution)? " yn
                case $yn in
                    [Yy]* )
                        if [ -e docker-compose.yml -a  -x docker-compose.yml]; then
                            docker-compose up
                            echo "OK!"                        
                        else
                            echo "ERR: compose file does not exist or missing exec permission, exiting.."
                            exit
                        fi
                    break;;
                    [Nn]* ) echo "Exiting.." exit;;
                    * ) echo "Please answer yes or no.";;
                esac
            done
        break;;
        [Nn]* ) echo "Exiting.." exit;;
        * ) echo "Please answer yes or no.";;
    esac
done


