import re
import os

class AssetItem:
    def __init__(
            self,
            original_path,
            updated_path,
            from_version,
            to_version
        ):
        self.original_path = original_path
        self.updated_path = updated_path
        self.from_version = from_version
        self.to_version = to_version
        self.layer_path = None
        self.can_be_updated = True
        self.should_be_updated = True
        
    
    # ----------------------------------OLD----------------------------------
def parse_payloads(self, content):
    # Simplified: focus only on @...usd[ac]@
    pattern = r"@[^@]+\.usd[ac]@(?:<[^>]+>)?"  
    matches = re.findall(pattern, content, re.IGNORECASE)
    seen = set()
    self.set_log(f"Found {len(matches)} payload(s)")
    
    for m in matches:
        # Remove optional target path
        clean_path = re.sub(r"<[^>]+>$", "", m) 
        m_norm = clean_path.lower()
        if m_norm in seen:
            continue
        seen.add(m_norm)
        item = self.find_latest_version_path(clean_path)
        if item:
            if item.from_version != item.to_version:
                self.listAssetsNeedUpdate.append(item)
                self.add_item_list(item)
            else:
                self.set_log(
                    f"🟰 Skipping up-to-date: {item.original_path}"
                )
        else:
            self.set_log(
                f"❌ Skipped (invalid or unresolvable): {clean_path}"
            )
            
            
def find_latest_version_path(self, original_path):
    path_pattern = (
        r"@(?P<base>.+?/Export/.+?/)"
        r"v(?P<version>\d{3})/"
        r"(?P<asset_name>.+)_.+?_"
        r"(v\d{3}\.usd[ac])@"
    )
    match = re.match(
        path_pattern,
        original_path,
        re.IGNORECASE
    )
    if not match:
        return None

    base_dir = match.group("base").replace("/", os.sep)
    current_version = int(match.group("version"))
    asset_name = match.group("asset_name")

    if not os.path.exists(base_dir):
        return None

    versions = [int(folder[1:]) for folder in os.listdir(base_dir)
                if re.fullmatch(r"v\d{3}", folder)]
    if not versions:
        return None

    latest_version = max(versions)
    latest_str = f"v{latest_version:03d}"
    latest_folder = os.path.join(base_dir, latest_str)

    for fname in os.listdir(latest_folder):
        fullmatch = re.fullmatch(
            f"{re.escape(asset_name)}_.+?_{latest_str}\\.usd[ac]",
            fname,
            re.IGNORECASE
        )
        if fullmatch:
            latest_path = f"@{match.group('base')}/{latest_str}/{fname}@"
            return AssetItem(
                original_path,
                latest_path,
                current_version,
                latest_version
            )
    return None
