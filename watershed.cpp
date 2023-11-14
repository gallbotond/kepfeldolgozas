void Watershed()
{
    const uchar bits[8] = {1, 2, 4, 8, 16, 32, 64, 128};
    // a kifelé folyás irányainak x és y komponense
    const int dx[8] = {1, 1, 0, -1, -1, -1, 0, 1};
    const int dy[8] = {0, -1, -1, -1, 0, 1, 1, 1};
    // betöltjük a szegmentálandó színes képet
    Mat imColor = imread("3.jpg", 1);
    // készítünk belőle egy szürke verziót
    Mat imO(imColor.cols, imColor.rows, CV_8UC1);
    cvtColor(imColor, imO, CV_BGR2GRAY);
    imshow("Szines", imColor);
    waitKey();
    imshow("Szurke", imO);
    waitKey();
    // Ez a kép tárolja majd a kiszámított gradiens értéket minden képpontban
    Mat imG = imO.clone();
    // Ez a kép tárolja majd minden képpont szomszédságában található legkisebb gradiens értéket
    Mat imE = imO.clone();
    // Ez a kép tárolja a kifele folyás irányát minden képpontban
    Mat imKi = imO.clone();
    // Ez a kép tárolja a befele folyás irányait (bitenként) minden képpontban
    Mat imBe = imO.clone();
    //
    // A szegmentált kép lesz (vízgyűjtők átlagolt színével)
    Mat imSegm = imColor.clone();
    // A szegmentált kép lesz (vízgyűjtők medián színével)
    Mat imSegmMed = imColor.clone();
    // Bináris kép mely megmutatja, hogy melyik képpontokban állítottuk már be a kifele folyást
    Mat imMap = imO.clone();
    // Gradiensek számításához használt 16 bites előjeles kódolású kép
    Mat imL(imColor.cols, imColor.rows, CV_16SC1);
    // felbontjuk a színes képet színcsatornáira
    vector<Mat> imColors;
    split(imColor, imColors);
    // A bemeneti kép három színcsatornáját fogjuk itt tárolni, ezekből számoljuk a gradienseket
    Mat imRed = imColors[2];
    Mat imGreen = imColors[1];
    Mat imBlue = imColors[0];
    // Ezen a képen összegezzük a három színcsatorna gradienseit
    Mat imSum = imO.clone();
    imSum.setTo(Scalar(0));
    // kék színcsatorna gradienseit adjuk hozzá az imSum-hoz
    Sobel(imBlue, imL, imL.depth(), 1, 0);
    convertScaleAbs(imL, imE);
    Sobel(imBlue, imL, imL.depth(), 0, 1);
    convertScaleAbs(imL, imG);
    add(imE, imG, imG);
    addWeighted(imSum, 1, imG, 0.33333, 0, imSum);
    // ződ színcsatorna gradienseit adjuk hozzá az imSum-hoz
    Sobel(imGreen, imL, imL.depth(), 1, 0);
    convertScaleAbs(imL, imE);
    Sobel(imGreen, imL, imL.depth(), 0, 1);
    convertScaleAbs(imL, imG);
    add(imE, imG, imG);
    addWeighted(imSum, 1, imG, 0.33333, 0, imSum);
    // vörös színcsatorna gradienseit adjuk hozzá az imSum-hoz
    Sobel(imRed, imL, imL.depth(), 1, 0);
    convertScaleAbs(imL, imE);
    Sobel(imRed, imL, imL.depth(), 0, 1);
    convertScaleAbs(imL, imG);
    add(imE, imG, imG);
    addWeighted(imSum, 1, imG, 0.33333, 0, imG);
    // Az összesített gradiens az imG képbe került
    // Előfeldolgozási lépés, amelyek közül csak egyiket használjuk
    // 1 - gradiensek csonkolása
    // cvCmpS(imG, 32, imE, CV_CMP_LT);
    // cvSub(imG, imG, imG, imE);
    // 2 - a gradiensek kisimítása egy Gauss-féle aluláteresztő szűrővel
    GaussianBlur(imG, imG, Size(9, 9), 0);
    imshow("Gradiens", imG);
    waitKey();
    // Step 0 - inicializálás
    // Erodált gradiensek kiszámítása - a szomszédságban levő legkisebb gradiensek kiszámítása
    erode(imG, imE, getStructuringElement(MORPH_RECT, Size(3, 3)));
    // A szegmentált képeket inicializáljuk egy szürke árnyalattal, ezeket elvileg mind felül fogja írni az algoritmus
    imSegm.setTo(Scalar(50, 50, 50));
    imSegmMed.setTo(Scalar(150, 150, 150));
    // Egyik pixelnél sincs befelé folyás kezdetben
    imBe.setTo(Scalar(0));
    // Valódi kifelé folyási irányok: 0..7, 8 azt jelenti, hogy az adott pixelnél még nincs eldöntve a kifelé folyás iránya
    imKi.setTo(Scalar(8));
    // Kezdetben sehol nincs még eldöntve a kifelé folyás iránya
    imMap.setTo(Scalar(0));
    // Step 1 - keressük meg és kezeljük le az összes képpontot, ahol a gradiens térkép lejtős
    // Bejárjuk a képet (x,y)-nal
    for (int x = 0; x < imBe.cols; ++x)
    {
        for (int y = 0; y < imBe.rows; ++y)
        {
            int fp = getGray(imG, x, y);
            int q = getGray(imE, x, y);
            // ahol az erodált gradiens kisebb a lokális gradiensnél, ott lejtős helyen vagyunk
            if (q < fp)
            {
                // megkeressük, hogy melyik irányba a legmeredekebb a lejtő
                for (uchar irany = 0; irany < 8; ++irany)
                {
                    // létezik-e a vizsgált koordinátájú szomszéd
                    if (x + dx[irany] >= 0 && x + dx[irany] < imBe.cols && y + dy[irany] >= 0 && y + dy[irany] < imBe.rows)
                    {
                        int fpv = getGray(imG, x + dx[irany], y + dy[irany]);
                        // ha az adott irany szerinti szomszéd gradiense annyi mint a minimum gradiens a szomszédságban...
                        if (fpv == q)
                        {
                            //...akkor beállítjuk a kifelé folyást az adott szomszéd irányába
                            setGray(imKi, x, y, irany);
                            // bejelöljük, hogy az (x,y) képpontban megvan a kifelé folyás iránya
                            setGray(imMap, x, y, 255);
                            // kiolvassuk a befelé folyás bitjeit a szomszédban...
                            uchar volt = getGray(imBe, x + dx[irany], y + dy[irany]);
                            // megmódosítjuk ...
                            uchar adunk = bits[irany];
                            uchar lesz = volt | adunk;
                            // és visszaírjuk
                            setGray(imBe, x + dx[irany], y + dy[irany], lesz);
                            break;
                        }
                    }
                }
            }
        }
    }
    // megmutatjuk egy ablakban a lekezelt képpontok térképét és várunk gombnyomásra
    imshow("Ablak", imMap);
    waitKey();
    // Step 2 - fennsíkon levő pontok lekezelése a gradiens térképen
    // Kell egy FIFO lista amire képpontokat fogunk elhelyeni
    Point *fifo = new Point[imBe.cols * imBe.rows];
    int nextIn = 0;
    int nextOut = 0;
    // Bejárjuk a képet (x,y)-nal
    for (int x = 0; x < imBe.cols; ++x)
    {
        for (int y = 0; y < imBe.rows; ++y)
        {
            // olyan képpontot keresünk, ahol már el van döntve a kifelé folyás iránya de van olyan szomszédja,
            // ahol még nincs eldöntve
            int fp = getGray(imG, x, y);
            int pout = getGray(imKi, x, y);
            if (pout == 8)
                continue;
            // találtunk egy olyan képpontot, ahol a kifelé folyás iránya már el van döntve ...
            int added = 0;
            // ... és vizsgáljuk annak a szomszédjait
            for (uchar irany = 0; irany < 8; ++irany)
            {
                if (x + dx[irany] >= 0 && x + dx[irany] < imBe.cols && y + dy[irany] >= 0 && y + dy[irany] < imBe.rows)
                {
                    int fpv = getGray(imG, x + dx[irany], y + dy[irany]);
                    int pvout = getGray(imKi, x + dx[irany], y + dy[irany]);
                    if (fpv == fp && pvout == 8)
                    {
                        // ha ide jutunk, akkor találtunk olyan szomszédot, ahol még nincs eldöntve a kifelé folyás iránya
                        // az ilyen (x,y) képpontokat felvesszük a FIFO listára
                        if (added == 0)
                            fifo[nextIn++] = Point(x, y);
                        added++;
                    }
                }
            }
        }
    }
    // amíg ki nem ürül a FIFO lista
    while (nextOut < nextIn)
    {
        // kiveszünk egy képpontot a listáról
        Point p = fifo[nextOut++];
        int fp = getGray(imG, p.x, p.y);
        // megkeressük az összes olyan szomszédját, ahol még nincs eldöntve a kifolyás iránya
        for (uchar irany = 0; irany < 8; ++irany)
        {
            if (p.x + dx[irany] >= 0 && p.x + dx[irany] < imBe.cols && p.y + dy[irany] >= 0 && p.y + dy[irany] < imBe.rows)
            {
                int fpv = getGray(imG, p.x + dx[irany], p.y + dy[irany]);
                int pvout = getGray(imKi, p.x + dx[irany], p.y + dy[irany]);
                if (fp == fpv && pvout == 8)
                {
                    // bejelöljük a kifelé folyás irányát a szomszédtól felénk
                    setGray(imKi, p.x + dx[irany], p.y + dy[irany], (irany + 4) % 8);
                    // bejelöljük, hogy a szomszéd képpontban megvan a kifelé folyás iránya
                    setGray(imMap, p.x + dx[irany], p.y + dy[irany], 255);
                    // bejelöljük a befelé folyás irányát
                    setGray(imBe, p.x, p.y, bits[(irany + 4) % 8] | getGray(imBe, p.x, p.y));
                    // az újonnan bejelölt szomszéd felkerül a listára
                    fifo[nextIn++] = cvPoint(p.x + dx[irany], p.y + dy[irany]);
                }
            }
        }
    }
    // megmutatjuk az ablakban a lekezelt képpontok térképét és várunk gombnyomásra
    imshow("Ablak", imMap);
    waitKey();
    // Step 3 - megkeressük a völgyekhez tartozó képpontokat a gradiens térképen
    // Keresünk olyan képpontot, amilyikből még nincs bejelölve a kifelé folyás iránya
    // Az ilyen képpontot kinevezzük lokális minimumnak és megkeressük körülötte azon
    // pontokat, amelyiknek még nincs kifelé folyása, ezekből mind a lokális minimum felé fog folyni a víz
    // Szükségünk van egy veremre
    Point *stack = new Point[imBe.cols * imBe.rows];
    int nrStack = 0;
    // Bejárjuk a képet (x,y)-nal
    for (int x = 0; x < imBe.cols; ++x)
    {
        for (int y = 0; y < imBe.rows; ++y)
        {
            int fp = getGray(imG, x, y);
            int pout = getGray(imKi, x, y);
            // Amelyik képpontban már megvan a kifelé folyás irányam azzal nem kell foglalkozni
            if (pout != 8)
                continue;
            // pout egy lokális minimumnak lesz kinevezve
            // Megkeressük azokat a szomszédokat, amelyeknek még nincs meg a kifelé folyási irányuk
            for (uchar irany = 0; irany < 8; ++irany)
            {
                if (x + dx[irany] >= 0 && x + dx[irany] < imBe.cols && y + dy[irany] >= 0 && y + dy[irany] < imBe.rows)
                {
                    int fpv = getGray(imG, x + dx[irany], y + dy[irany]);
                    int pvout = getGray(imKi, x + dx[irany], y + dy[irany]);
                    if (pvout == 8 && fp == fpv)
                    {
                        // itt találtunk olyan szomszédot
                        // bejelöljük a kifelé folyást a lokális minimum felé
                        setGray(imKi, x + dx[irany], y + dy[irany], (irany + 4) % 8);
                        setGray(imMap, x + dx[irany], y + dy[irany], 255);
                        setGray(imBe, x, y, bits[(irany + 4) % 8] | getGray(imBe, x, y));
                        // a szomszéd képpontot betesszük a verembe
                        stack[nrStack++] = cvPoint(x + dx[irany], y + dy[irany]);
                    }
                }
            }
            // amíg ki nem ürül a verem
            while (nrStack > 0)
            {
                // kiveszünk egy képpontot és megnézzük, hogy a szomszédai között van-e olyan, akinek nincs megjelölve a
                // kifelé folyás iránya
                Point pv = stack[--nrStack];
                int fpv = getGray(imG, pv.x, pv.y);
                int pvout = getGray(imKi, pv.x, pv.y);
                for (uchar irany = 0; irany < 8; ++irany)
                {
                    if (pv.x + dx[irany] >= 0 && pv.x + dx[irany] < imBe.cols && pv.y + dy[irany] >= 0 && pv.y + dy[irany] < imBe.rows)
                    {
                        // itt találtunk létező szomszédot
                        int fpvv = getGray(imG, pv.x + dx[irany], pv.y + dy[irany]);
                        int pvvout = getGray(imKi, pv.x + dx[irany], pv.y + dy[irany]);
                        // if (fpv==fpvv && pvvout==8 && (!(pv.x+dx[pvout]==x && pv.y+dy[pvout]==y)))
                        if (fpv == fpvv && pvvout == 8 && (!(pv.x + dx[irany] == x && pv.y + dy[irany] == y)))
                        {
                            // itt találtunk olyan szomszédot
                            // bejelöljük a kifelé folyást pout felé
                            setGray(imMap, pv.x + dx[irany], pv.y + dy[irany], 255);
                            setGray(imKi, pv.x + dx[irany], pv.y + dy[irany], (irany + 4) % 8);
                            setGray(imBe, pv.x, pv.y, bits[(irany + 4) % 8] | getGray(imBe, pv.x, pv.y));
                            // a szomszéd képpontot betesszük a verembe
                            stack[nrStack++] = Point(pv.x + dx[irany], pv.y + dy[irany]);
                        }
                    }
                }
            }
        }
    }
    // megmutatjuk az ablakban a lekezelt képpontok térképét és várunk gombnyomásra
    // itt már csak izolált fekete képpontok lesznek a fehér képen, ezek a lokális minimumok
    imshow("Ablak", imMap);
    waitKey();
    // Step 4
    // feltérképezzük a vízgyűjtő medencéket a lokális minimumokból kiindulva a víz folyásával fordított irányba haladva
    // minden vízgyűjtő medencében kiszámoljuk az átlagos és a medián színt
    // mindkettőből generálunk egy-egy külön kimeneti szegmentált képet
    // ez a puffer a medián számításához kell
    uint *medbuff = new uint[imBe.cols * imBe.rows];
    int label = 0;
    nextIn = 0;
    int spotSum[3];
    // Bejárjuk a képet (x,y)-nal
    for (int x = 0; x < imBe.cols; ++x)
        for (int y = 0; y < imBe.rows; ++y)
        {
            // keresünk lokális mimimumot
            int pout = getGray(imKi, x, y);
            if (pout != 8)
                continue;
            // találtunk lokális mimimumot, betesszük a verembe
            stack[nrStack++] = Point(x, y);
            for (int i = 0; i < 3; ++i)
            {
                spotSum[i] = 0;
            }
            // amíg üres nem lesz a verem
            while (nrStack > 0)
            {
                // Kiveszünk egy képpontot a veremből és megnézzük, honnan folyik felénk a víz
                // Ahonnan felénk folyik a víz, azt a képpontot felvesszük az aktuális régióba és
                // betesszük a verembe is.
                Point pv = stack[--nrStack];
                fifo[nextIn++] = pv;
                uchar r, g, b;
                getColor(imColor, pv.x, pv.y, r, g, b);
                spotSum[0] += (int)b;
                spotSum[1] += (int)g;
                spotSum[2] += (int)r;
                uint o = (int)r * 0x10000 + (int)g * 0x100 + (int)b;
                o += (uint)(round((float)r * 0.299 + (float)g * 0.587 + (float)b * 0.114) * 0x1000000);
                medbuff[nextIn - 1] = o;
                // setGray(imLabel, pv.x, pv.y, label);
                int pvin = getGray(imBe, pv.x, pv.y);
                for (uchar irany = 0; irany < 8; ++irany)
                {
                    if ((bits[irany] & pvin) > 0)
                    {
                        // setGray(imLabel, pv.x + dx[(irany + 4) % 8], pv.y + dy[(irany + 4) % 8], label);
                        stack[nrStack++] = Point(pv.x + dx[(irany + 4) % 8], pv.y + dy[(irany + 4) % 8]);
                    }
                }
            }
            // a label azt számolja, hogy hány régió van összesen a szegmentált képen
            label++;
            if (nextIn < 2)
                printf("%d", nextIn);
            for (int i = 0; i < 3; ++i)
            {
                spotSum[i] = round(spotSum[i] / nextIn);
            }
            // kiszámoljuk a medián színt a quicksort segítségével
            qsort(medbuff, nextIn, sizeof(uint), compare);
            int medR = (medbuff[nextIn / 2] % 0x1000000) / 0x10000;
            int medG = (medbuff[nextIn / 2] % 0x10000) / 0x100;
            int medB = (medbuff[nextIn / 2] % 0x100);
            for (int i = 0; i < nextIn; ++i) // if (getGray(imMask, fifo[i].x, fifo[i].y) > 128)
            {
                // itt festjük ki a régiót az átlagos színnel
                setColor(imSegm, fifo[i].x, fifo[i].y, (uchar)spotSum[2], (uchar)spotSum[1], (uchar)spotSum[0]);
                // itt festjük ki a régiót a medián színnel
                setColor(imSegmMed, fifo[i].x, fifo[i].y, (uchar)medR, (uchar)medG, (uchar)medB);
            }
            nextIn = 0;
        }
    // memória felszabadítás
    free(fifo);
    free(stack);
    free(medbuff);
    // no more steps
    printf("\nRegions: %d \n", label);
    // megmutatjuk egy ablakban a medián színekkel készített képet
    imshow("Median", imSegmMed);
    // megmutatjuk egy masik ablakban az átlagos színekkel készített képet
    imshow("Atlag", imSegm);
    waitKey();
}
