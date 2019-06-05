from unittest import TestCase

from burst.libs.multiout import MultiOutPack


class MultiOutTest(TestCase):
    def setUp(self) -> None:
        self.mo = MultiOutPack()

    def test_header_ok(self):
        # transaction #15440603410472198198
        data = b'\x01\x02\xfd\xb6\x06W\xaa\x8c\xa1\x88\xb6jG\xa4\x02\x00\x00' \
               b'\x00\xaf\xc6\xef\xdd;\xa2C\x8f\x1c\x11 \xd1\x00\x00\x00\x00'
        self.assertEqual(
            self.mo.unpack_header(data),
            (1, 2)
        )

    def test_multiout_ok(self):
        # transaction #15440603410472198198
        data = b'\x01\x02\xfd\xb6\x06W\xaa\x8c\xa1\x88\xb6jG\xa4\x02\x00\x00' \
               b'\x00\xaf\xc6\xef\xdd;\xa2C\x8f\x1c\x11 \xd1\x00\x00\x00\x00'
        self.assertEqual(
            self.mo.unpack_multi_out(data),
            (9845304923641001725, 11346078390, 10323273148873557679, 3508539676)
        )

    def test_multiout_same_ok(self):
        # transaction #7667547325904032098
        data = b'\x01q+\x89\xf2\x1a\x80\xd1\x08\x8eG*\xd9\xb5gc3L\x1d\xb9\x0cDF\x7f\xc4;\xa9C\xa2Djk\xcd\x14l\x04' \
               b'\xb5f;#b\x0b\x97\xb1\xfazG\x10Y\x8c\x975\xe8\x967\xd9-p\x15\xfd\xa2xd\xde\xbd\n\x8d\xdfo\xac)\x0f' \
               b'\xc6"\x94X\x07\xd9x\xc7\xe1\x03\xd5\xf0?\xc0\x9c\x8c\xdd5\xae\xf5\x900\x04\xaf\'U\xe5\x8e\xbe\xed' \
               b'\xf9\x1a(\xd4\x0f\x00\x8e\xbe\xdf\x0f\x1b\xa1(z\xc9\xd0i\xc2\xe3]\xe10\xdc]\xd5\\\xb8n\xc1|\x01nk' \
               b'\xfd\xba/\xd2iT\xb3\xb7\xdd}[\xb0\xb9#\x08\xed@}!\x97\xb1\x9aKp\x930\xb8\xdbwT\x9c\nO\xfd8\xee\xb1' \
               b'\xe3\xd8\xac(\xc9.\x9b\x92\xe6\x9cR\']yJ\xb1\xae\xd9k\xaa\xb8{\xc2G\xf7\xb8\xae\xa4\xcb\x00\\Q\xcd%' \
               b'\x80\x7f\xe0\xe4\xec\x8a\xc1\xf7\x88\\\x9c?/h\x7f\xdd\x9at\xf1\xa3\x17+\xfa\xa4\x99\xc26\xab\xc1' \
               b'\x19M\x99\x1c\x8bY^\xd9\x81\xe6z\xd3\x9d\xc0\xbc\xdb\x0f9n\x98y\x96"\xb4\xd9\x03q\xdcw\xc6\xf4\xaf' \
               b'\x89\xdcD\xf6\xf0\x90"O\xb1\xecq\x08B\xd0\x19\x87\x1c\xfc\xcb\xd5\xc4\x85n\r\xa8\x15\xed\x01}\x1d' \
               b'\xb3$\x8a\x99L\x8f\xbfF\x8bn\xae\x97\x0e\xa3J\x8a\x8dW\x86\xde\x16\x1b\x1b\xa6V\xa3\xe7\x89\xb8\x19' \
               b'\xcdZ?;L\xe9ock\xa7\xf7H\xde[|H\xa6\xde\xcf/\xcb\xe2\x81\x1e.1\xdaK\xfc\xa6\xd0\xe8\xd0R3\xfc\xffeKe' \
               b'\xa8n4;\xd5%OX\xc3\xdd\xd1.\x13QwI\xdbM\x8bO\x82\xec\x07\x0c\xf3#\xc6\xa8M\x98\xdb\x85\x07\xc2"\r' \
               b'\xcbC\xb9\xd8\\\xcd+\xce6\xd8\xff:\xc2\xc7:6\x90)\xb3M\xe7r\x02_\xea\xeb+\xd9\xc0U\xb7\xa1#\xe5R1' \
               b'\\"\xbcUnGC8\n\xb29\xb9\x08j\x81\xdbbt.~\xbf\xd0\x0c>{Uf\x03\x9fV\x08%\x811\xc2]8\x19\xbf-\xd6' \
               b'\x89K\x9f\xe7\'7\xff\xf0\xc7\xad05\x10\xc8\xc6\xa4\x11\x870g\xc7\x1f\xde\x84\x1a\x10\xe8\xbf\xacJ)\r' \
               b'\x9f6\x82\x9c\x1b\xcd\xb5[\xcd;N\xb0\xcf\x08D&\xc3M\x7f)\n\xf4\x8bd:\x1d\xcc\x04!6\xd3h1\x86\x8a\xa3' \
               b'\x8d\x95\x94/KWmS\x1b\t\xb1\xb8vK\xf8\xd0\x90q\xb4\x1cO\x83\xfaJ\xe6\x02\xa9\xe0\xbb\xa5\x14m\x06' \
               b'\xbb\xd4\x18\x9a9\x87\xaf|w1\x8bqx\x1f\xbfb\xda\xc3s\xb1&\xff\\Zgi\x06\xab\x07\x9e\xa9\xd0J1j\xc6' \
               b'\xf7\xfe#\x0b\xad\xf1\x12\x06\xd3\x19\xd8E\x1ah\xf6\x98}[a\xbb\xe3a\xd1|\xe2\x85$\x1b\xb1_\xf0\xc6' \
               b'\x98\x9f0,\xa1\x185"\x0c\x10\xa4\xb8\xaa\xbeL\xe4\x96\xf6\xd4\xf0\x82\xc6z\x1c\xbd\xf0\x87\xed' \
               b'\xfe5t\x7f=+\xfc\xd7\x07\x16#_p\xa0\x0e\xaa3\x0bY\x87\xbe\x0c\x12\xb7\xd9\xe6\x13\xe80\x12\x0c$\x12' \
               b'\xa9j\xb2%md\xb7\xec&v\xa4N\x9d\xa5xL\xbb\xa7"g\xc2\x8c3\x01\x9be\xf0W`\xf1\xa9=\xc5V\xb5\xcdJE!\x9a' \
               b'\xfe\x1d\x0e\xb06L:\xe3\xb2\xef\x01{(tU\x9b\x98\xdb%\xc0\xa2?\x05\xdeLE\xafU-\xea\x977M\x815G\xd5V' \
               b'\x92\xce\xf7iZ\xf2\xe1\xafYE\x94\xf1\xe5[B\xf6\x12\xc1\xfc\xacf\x05\xb2Z\xf6\xd0\x9c\xa8,\xc2?\x99' \
               b'\x17\xc3\x93(tf=\x1a\xf4\x19\x8f\x83x\xdb7\xbb\xa4\xcbr\x02\xcfD\xa61\x1d\xab[[\xef\xe0\xaaIy\xff' \
               b'\xad\xd6\xc1\xb0bsT*\xfc\xf5\xdc\xda\\\xa43\xd1\xbc\\\xf2\x1d\x91\x84\x12S\xd1\x92|\xa8\x96U\x87' \
               b'\x9ec\x9d\x96\xad\xb9\x86\x93\xa1\x9b\xe6_E\xeb(\xc9d\xd7\xf5n\xa3'
        self.assertEqual(
            self.mo.unpack_multi_out_same(data),
            (10234660501337573675, 5490841667778456135, 4306707083439159581, 1498972355146433449, 820256820168033388,
             10113132337429131671, 8083355738978137495, 774019234079636757, 2505706914339348365, 279723973724821652,
             3881413058731438293, 6136065449845126574, 15287498595847016165, 11608889918126686223, 6765464824970836520,
             7978228811359334625, 3439339903299714241, 6592669210597681618, 2413156362128439728, 13272270212374901143,
             4106525342222809051, 3371270518901813742, 8745189287196529307, 8915062842570223946, 57320490606741442,
             16492322023797510492, 4583640264098286316, 11813351506059421743, 12337262194381695767, 6798618067439786433,
             13601044406284485081, 2492313139387371483, 17637916779315714484, 2490755534443809199, 1860059250142523727,
             7963987938603965575, 12906609554339768333, 10035919441828088356, 10199046370318855790, 6243707736557520471,
             4565186682647340963, 17845350123302374459, 14978592240935099976, 15722398482690132783, 3698247942376193099,
             3778142290420563964, 15122457907832411451, 10037920253059601198, 14277522476692701775, 2504572614267653544,
             3156280999747504909, 4235567533221492430, 176457656325214262, 13210677120938535519, 13556499195252515745,
             4157396642779590229, 3347409117951690937, 7373935471322251134, 13993107513270509315, 5443117116621928541,
             12522242267859642271, 9732741443391337776, 1160385943552091952, 3935879070342758376, 4309201254851779714,
             5603364435026489422, 2106106328006666623, 9669625131296687308, 6290173619763782538, 5437736670597960557,
             9461812903453708536, 11942385853405743866, 4150657308525227284, 8678871001493974919, 2788136929338769183,
             552542429058325759, 17854074532698040734, 15205862021062665214, 9050254378178828313, 16320149368046575963,
             11008750632937661573, 874319657562812575, 10872899782170944528, 13626901565535212790, 4431388333614925808,
             8097229232563289131, 13729039893708541600, 3524088590633472524, 2716350799644199954, 5666784140691203181,
             7431686757998437789, 6336676392124779714, 14822849153702949216, 12686110179694036298, 8863629093237312566,
             13845714077908038696, 6174229810592956322, 5131149519103715885, 17463387018126055125, 6621964446239141857,
             389188619385108034, 13991743533807458994, 7382570304265492799, 15814534742150486589, 4958184406824303415,
             16208274033200673190, 12736697263984298410, 15770750458535375714, 2157889137497318492,
             12140740123223557265, 12508358066255123862, 4998967667509659321, 11776620381078104299)
        )
