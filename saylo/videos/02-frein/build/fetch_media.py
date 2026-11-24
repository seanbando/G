"""Rebuild saylo/videos/02-frein/media/ from the creator's Google Drive folder "Frein" (link-shared).
    python saylo/videos/02-frein/build/fetch_media.py
Every Drive file goes to media/src/ under the name the plans expect; photos are also copied to media/photos/ under
their plan name. Files already on disk with the right size are skipped. Cut-outs (media/cuts/) are not made here."""
import os, shutil, sys, urllib.request

VID = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SRC = os.path.join(VID, "media", "src")
PHO = os.path.join(VID, "media", "photos")
URL = "https://drive.usercontent.google.com/download?id=%s&export=download&confirm=t"

# (Drive file id, size in bytes, Drive title, name in media/src or None = keep the title, name in media/photos or None)
FILES = [
    # videos
    ("1NPtg6ExSncU2-v0Wmqo8pQSFrsHf4S2j", 25284573, "Search for alleged cop killer instills fear in Pa. community - CBS Evening News (720p, h264).mp4", None, None),
    ("1_hCD1BpdLLhWrGthauEdHok0t247z1K7", 30041152, "Slain cop's cuffs used to arrest Frein - CNN (720p, h264).mp4", None, None),
    ("1EW1P5Mj83qaqC8h7ahtohMRunXzhelxq", 31151110, "Authorities Identify Suspect in Pennsylvania Barracks Shooting - ABC News (720p, h264).mp4", None, None),
    ("1HXyngOoKsM5vK3paIp2hU63sqeUBQJ0_", 21470461, "Eric Frein manhunt Suspect may have left letter - CBS Evening News (720p, h264).mp4", None, None),
    ("1yrLqEGsdQ54M552eZqOPpxa3vQfIZHm7", 22809403, "Pa. breathes easier after capture of Eric Frein - CBS Evening News (720p, h264).mp4", None, None),
    ("10ZN86X_WXZpD6cZ4ZBcSHHPIHk1st1Ff", 35261002, "Police discovers journal of Pennsylvania cop killer suspect - CBS Mornings (720p, h264).mp4", None, None),
    ("1n_ELODyWhiihFwaSFR7HBGfCOM_ku2r1", 152556361, "Pike County DA Ray Tonkin responds to Eric Frein's Sentence of Death - Straus News (1080p, h264).mp4", None, None),
    ("1SJM_Jn3edOxcnZrYk6Z0SDHfu3wWnbO6", 16836001, "Eric Frein Notice of Execution signed for man responsible for killing PA State Trooper - WTAJ News (1080p, h264).mp4", None, None),
    ("12jF3JSMoZcK5bWiR87TYlADgGNYsrAiA", 203259323, "Man Who Found Frein's Jeep Just Happy To Help _ wnep.com ... Microsoft Edge 2026-11-18 19-54-14.mp4", "wnep-novak-jeep-screen-recording.mp4", None),
    ("1HHkLR8zsyf9stWyCzq5wo60kPSb90Sp3", 86873830, "Screen Recording 2026-11-19 205026.mp4", "hangar-screen-recording-2026-11-19.mp4", None),
    # photos and screenshots
    ("1ugcehj-lcT07zvpfBrCx_G-Pn3ueAaPP", 25963, "Eric_Frein ( wikimedia commons).jpg", None, None),
    ("1GIvIg-7IVv3K2U0v5oBR6cSFaNCaIc0m", 25963, "fbi wanted poster.jpg", None, None),
    ("1pSlMASBgDxKBLqL0Y3Hyg9Qf03RqCJcB", 303287, "default.jpg", None, "09d-campsite-default.jpg"),
    ("1M2sumeGkE3pqeeIMg8qVgQMk_Psz4WQO", 419382, "phillymag.jpg", None, "11c-phillymag-perp-walk-night.jpg"),
    ("1xR06aVVOI2f6-omXo-1WhtdsbQAH0MoK", 274059, "13b-cbs-halloween-headline.png", None, "13b-cbs-halloween-headline.png"),
    ("1dDYQ8slkN88UGSVQadoET4qmwrBWVPiF", 31054, "dailylocal.webp", None, "14-dailylocal.webp"),
    ("1jhTiML_wlE1UpNPkgSZqBUkdraqKesJp", 308485, "buzzfeednews.png", None, "18b-buzzfeednews-fbi-page.png"),
    ("1-48bEvt7BaeLrlmpcEN92qjguHTpVll3", 387478, "19a-court-opinion-p28-silence-ruling.png", None, "19a-court-opinion-p28.png"),
    ("1omefhpFpViX-PH2D6tpwbZjiJNPWcs4n", 405372, "19b-court-opinion-p29-dna-ballistics-handwriting.png", None, "19b-court-opinion-p29.png"),
    ("1AYrozZEUXUqbuAMm8uyjGv2nMCCnSpI2", 267264, "19c-court-opinion-p1-caption.png", None, "19c-court-opinion-p1-caption.png"),
    ("1qGKJbVG1V7PTaFGW_9lfh8eLkJXozPdp", 109275, "20-inquirer-got-a-shot-headline.png", None, "20-inquirer-headline.png"),
    ("1kKEf8NA9ejVPWIC1Bj3Nij6B8Wmy_yq5", 685233, "23-courthouse-milford.jpg", None, "23-courthouse-milford.jpg"),
    ("1EaEbFg_9miM93lxWNO4e_QekqP7SwBmo", 531021, "24-psp-taurus.jpg", None, "24-psp-taurus.jpg"),
    ("1Sul11U6kFh346-IIJBcdIWoA-TNZlKue", 880129, "25-canadensis.jpg", None, "25-canadensis.jpg"),
    ("1islCZfc_qypq2BQEhVSgX_g2YZaC0_0u", 1658472, "26a-tannersville-bog-forest.jpg", None, "26a-bog-forest.jpg"),
    ("1nuRbTIi-fXx7Oe-tqsM4GmGU4tdLC4uq", 1178119, "26b-tannersville-bog-forest.jpg", None, "26b-bog-forest.jpg"),
    ("1QIQWNVXQ0J6tN-oa4QPKLinC_5jdmZ-7", 375759, "26c-big-pocono-view.jpg", None, "26c-big-pocono-view.jpg"),
    ("1nWYjEsKmCiu17xu6DEiZfT37suArkIY5", 1101396, "ap_eric_frein_manhunt_jeep_swamp_jc_140925.jpg", None, "27c-jeep-swamp-ap.jpg"),
    ("1kkM6lgfbwKxGNJWZbLf_IY4oc1AM1MmT", 139346, "6ES2HI47JNA37L5P6Y3TMHO65A.webp", None, "30-troopers-rifles-6ES2.webp"),
    ("1UqT8jf4d5ovgtDEfM9L56AZG6Rkcooax", 95334, "ABC_pa_manhunt_inset_mar_140917_16x9_992.jpg", None, "31-abc-roadblock-inset.jpg"),
    ("1vpxpOy1g4FUt6sodawI3_ZVPYK27Lx-1", 81413, "AP_eric_frein_ml_141031_16x9_992.jpg", None, "32-ap-perp-walk.jpg"),
    ("1RYYjQNgd1YUKB8BiGvwdnC3Gk6zBF69z", 151081, "thecitizensvoice.jpg", None, "33-thecitizensvoice-cruisers-field.jpg"),
    ("1Hk1qvAMKACFXiKzT19K4x1eufKpujnNt", 793784, "PPO235GMEVB27GRUQ6RO45DUDA.jpg", None, "34-armored-PPO235.jpg"),
    ("1ZKjeMNU2_8sDkh5let3CoiACrEWMSpvf", 111958, "ghows-PR-2ef2e814-5c19-47e7-b680-b0fff28eafe5-88f724df.webp", None, "35-tactical-team-ghows.webp"),
    ("1ljHCX6SXXJqPE-Iw-yqzRhuna8Usj5ha", 172118, "abcnewsgo.jpg", None, "36-abcnewsgo.jpg"),
    ("12hFd_2RyfxXpCetbhOcjwaeZJb_Ncl7w", 38824, "poconorecord.webp", None, "41-poconorecord.webp"),
    ("1DDwMfkmAs-oiZdKYX01JI69IX5UYMEoW", 483822, "7Y7YM5UUMJABTJWJ2GGQDKCW4I.jpg", None, "7Y7YM5UU.jpg"),
    ("1kKqUkJedNMm-DJy4RhyGqk-_HY6pIQyZ", 1542054, "AP_eric_frein_manhunt_1_sk_141001.jpg", None, "AP-manhunt-snow-hill-road.jpg"),
    ("1vFQ5MxjgHMHpeTd_SJf0HBBhrIGCDLcR", 249120, "TMC-L-FreinManhunt-109970512.webp", None, "TMC-FreinManhunt-troopers-stage.webp"),
    ("1gPx29KZvHEbqhO_GFRcsDJdYebSDRUJx", 168959, "ca-times.brightspotcdn.jpg", None, "ca-times-brightspot.jpg"),
    ("1xCWKjwD051-x0f3iyaSiDAgm2DTKUV1c", 140876, "1415226383337_wps_34_An_exterior_view_of_the_h.jpg", None, "hangar-exterior.jpg"),
    ("1-6FFZYs-hSqDjuFOmgLyq1j9OqdSwQ8s", 705758, "abcnews - RT_eric_frein_hangar_interior_1_jt_141102.jpg", None, "hangar-interior-reuters-abc.jpg"),
    ("1588gwEBBzBVSWykL7HoSGbVlwIj8NPhD", 39854, "poconos.webp", None, "poconos.webp"),
    ("1TryzJp6c6tLRJr26Nzg1jqONvCpQ6cIx", 130380, "cnn funeral.webp", None, None),
    ("1VWSKC3TwnLF8pGPTbSGsUnp0UjFAYASD", 18532, "troopers KDVR.webp", None, None),
    ("1uheVlLJ0CHxHxydulUqv1rpWWlJ06oMS", 37288, "OIP.webp", None, None),
    ("1W2JolnbvoHDoZw3sPG8elPNOjSiaGyVI", 44187, "alex douglas tpt.avif", None, None),
    ("1chUWaU_Mu4lV6zJmQ7WyaBGdLbGcy2o6", 647011, "Screenshot 2026-11-18 221017.png", None, None),
    # two files share each of these Drive titles: -a = uploaded first, -b = uploaded second
    ("1uhKlpK8Cd3D-SLvO6b6ma80Op1Ola_fz", 289319, "wnep.jpg", "wnep-a.jpg", "wnep-a.jpg"),
    ("1TGKEzLy0e_tcIehdWCea747Nsg-qUh4j", 274770, "wnep.jpg", "wnep-b.jpg", "wnep-b.jpg"),
    ("1niZM4wi_1EGnhGhis8CW7sUteu45010c", 31002, "mcall.webp", "mcall-a.webp", "mcall-a.webp"),
    ("1hvDQcSGizB-gOEaIphChenwOx4icOSNM", 28126, "mcall.webp", "mcall-b.webp", "mcall-b.webp"),
    ("1yKUQUV270NuMagBQt8nnASvEyE5ujhZz", 42202, "pikecountycourier.webp", "pikecountycourier-a.webp", "pikecountycourier-a.webp"),
    ("1rhdUjrmUpsD4f_7dqx8hZlcP1rjpwkJh", 42218, "pikecountycourier.webp", "pikecountycourier-b.webp", "pikecountycourier-b.webp"),
]


def main():
    os.makedirs(SRC, exist_ok=True)
    os.makedirs(PHO, exist_ok=True)
    bad = 0
    for fid, size, title, src_name, photo_name in FILES:
        dst = os.path.join(SRC, src_name or title)
        if not (os.path.exists(dst) and os.path.getsize(dst) == size):
            tmp = dst + ".part"
            with urllib.request.urlopen(URL % fid, timeout=120) as r, open(tmp, "wb") as f:
                shutil.copyfileobj(r, f, 1 << 20)
            got = os.path.getsize(tmp)
            if got != size:
                print("WRONG SIZE", got, "expected", size, "|", title)
                bad += 1
                continue
            os.replace(tmp, dst)
        print("ok", os.path.basename(dst), flush=True)
        if photo_name:
            shutil.copyfile(dst, os.path.join(PHO, photo_name))
    print("done,", bad, "problem(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
