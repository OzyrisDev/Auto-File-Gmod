import os

def create_precache_file(addon_path):
    precache_content = '''local particlename = {
    "exemple1",
    "exemple2",
}

for _, v in ipairs(particlename) do PrecacheParticleSystem(v) end
'''

    precache_file_path = os.path.join(addon_path, 'lua', 'autorun', 'precache_ozyris.lua')

    with open(precache_file_path, 'w') as f:
        f.write(precache_content)

def create_weapon_files(weapons_path, weapons_name, print_name, category):
    init_lua_content = f'''AddCSLuaFile("cl_init.lua")
AddCSLuaFile("shared.lua")
include("shared.lua")

function SWEP:Initialize()
	self:SetHoldType("normal")
end

timer_Simple = timer.Simple 
timer_Create = timer.Create

function SWEP:PrimaryAttack()
    if self.{weapons_name} then return end
	self.{weapons_name} = true
	timer_Simple(2, function() if IsValid(self) then self.{weapons_name} = false end end)
	local ply = self.Owner 
end 

function SWEP:SecondaryAttack()
end

function SWEP:OnDrop()
	self:Remove() -- You can't drop fists
end
'''
    
    cl_init_lua_content = '''include("shared.lua") 
AddCSLuaFile() 

function SWEP:Initialize()
	self:SetHoldType("normal")
end

function SWEP:PrimaryAttack()
end

function SWEP:SecondaryAttack()
end
'''
    
    shared_lua_content = f'''SWEP.PrintName = "{print_name}"
SWEP.Category = "{category}"
SWEP.Author = "Ozyris"
SWEP.Purpose = "Swep de la mort qui tue par ozyris le boss"

SWEP.Slot = 0
SWEP.SlotPos = 4

SWEP.Spawnable = true

SWEP.ViewModel = Model( "" )
SWEP.WorldModel = ""
SWEP.ViewModelFOV = 54
SWEP.UseHands = true

SWEP.Primary.ClipSize = -1
SWEP.Primary.DefaultClip = -1
SWEP.Primary.Automatic = false
SWEP.Primary.Ammo = "none"

SWEP.Secondary.ClipSize = -1
SWEP.Secondary.DefaultClip = -1
SWEP.Secondary.Automatic = false 
SWEP.Secondary.Ammo = "none"

SWEP.DrawAmmo = false
'''
    
    with open(os.path.join(weapons_path, 'init.lua'), 'w') as f:
        f.write(init_lua_content)
        
    with open(os.path.join(weapons_path, 'cl_init.lua'), 'w') as f:
        f.write(cl_init_lua_content)
        
    with open(os.path.join(weapons_path, 'shared.lua'), 'w') as f:
        f.write(shared_lua_content)

def create_weapons(addon_path):
    while True:
        create_precache = input("Voulez-vous créer un fichier de precache ? (O/N): ")
        if create_precache.lower() == 'o':
            create_precache_file(addon_path)
        elif create_precache.lower() == 'n':
            pass
        else:
            print("Veuillez répondre par 'O' pour oui ou 'N' pour non.")
            continue

        create_weapons = input("Voulez-vous créer un dossier 'weapons' ? (O/N): ")
        if create_weapons.lower() == 'o':
            weapons_name = input("Veuillez entrer le nom du weapons : ")
            print_name = input("Veuillez entrer le nom à afficher in-game : ")
            category = input("Veuillez entrer la catégorie de l'arme : ")
            weapons_path = os.path.join(addon_path, 'lua', 'weapons', weapons_name)
            os.makedirs(weapons_path)
            create_weapon_files(weapons_path, weapons_name, print_name, category)
        elif create_weapons.lower() == 'n':
            break
        else:
            print("Veuillez répondre par 'O' pour oui ou 'N' pour non.")    

def create_addon_folder(addon_name):
    GESTURE_SLOT_CUSTOM = 0

    base_path = r"C:\Program Files (x86)\Steam\steamapps\common\GarrysMod\garrysmod\addons"
    
    addon_path = os.path.join(base_path, addon_name)
    
    os.makedirs(addon_path)
    
    subfolders = ['materials', 'lua', 'models', 'particles', 'sound']
    
    for folder in subfolders:
        os.makedirs(os.path.join(addon_path, folder))
    
    entities_path = os.path.join(addon_path, 'lua', 'entities')
    os.makedirs(entities_path)
    
    autorun_path = os.path.join(addon_path, 'lua', 'autorun')
    os.makedirs(autorun_path)
    os.makedirs(os.path.join(autorun_path, 'server'))
    os.makedirs(os.path.join(autorun_path, 'client'))
    
    with open(os.path.join(autorun_path, 'server', 'sv_ozyris.lua'), 'w') as f:
        f.write('''
local meta = FindMetaTable("Player")
                
util.AddNetworkString("Ozyris:SendAnim")  
                
function meta:SetAnim(anim)
    net.Start("Ozyris:SendAnim")
    net.WriteEntity(self)
    net.WriteString(anim)
    net.Broadcast()
end
                
                
                ''')

    with open(os.path.join(autorun_path, 'client', 'cl_ozyris.lua'), 'w') as f:
        f.write('''net.Receive("Ozyris:SendAnim", function()
    local ply = net.ReadEntity()
    local anim = net.ReadString()
    
    local val1, val2 = ply:LookupSequence(anim)
    if val2 == 0 then return end

    ply:AddVCDSequenceToGestureSlot(GESTURE_SLOT_CUSTOM, val1, 0, true)
end)''')
    
    create_weapons(addon_path)
    
    print(f"Dossier addon '{addon_name}' créé avec succès.")

if __name__ == "__main__":
    addon_name = input("Veuillez entrer le nom de l'addon : ")
    create_addon_folder(addon_name)
