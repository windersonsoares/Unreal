import unreal
import sys

# Biliotecas e utilidades da Unreal
levelLib = unreal.EditorLevelLibrary
levelUtils = unreal.EditorLevelUtils
actorUtils = unreal.EditorActorSubsystem
stringUtils = unreal.StringLibrary
systemLib = unreal.SystemLibrary
assetLibrary = unreal.EditorAssetLibrary
dataTableLibrary = unreal.DataTableFunctionLibrary
dataSmithLibrary = unreal.DatasmithContentLibrary

# Prefixos das tags
prefixTarefa = 'AYTF_'
prefixOrdem = 'AYOR_'
prefixQuantidade = 'AYQT_'

# region FUNÇÕES

def CriarTagComBaseNaMetadataFBX():

    print('CriarTagComBaseNaMetadataFBX')

    # Prefixos das tags
    prefixTarefa = 'AYTF_'
    prefixOrdem = 'AYOR_'
    prefixQuantidade = 'AYQT_'

    # Pega os atores selectionados
    actorSubSystem = unreal.get_editor_subsystem(actorUtils)
    selectedActors = actorSubSystem.get_selected_level_actors()

    # Endereço dos assets onde será procurado
    assetPath = '/Game/Meshes/LON_Unimed'

    # Pega os assets presentes no edereço
    assetRegistryHelper = unreal.AssetRegistryHelpers.get_asset_registry()
    assetRegistry = assetRegistryHelper.get_assets_by_path(assetPath, False, False)

    # Cria um dicionário com todos os assets e seus nomes como chaves
    dictAssetsNames = dict()
    for registry in assetRegistry:
        asset = registry.get_asset()
        assetName = systemLib.get_object_name(asset)
        dictAssetsNames[assetName] = asset

    # Para cada ator selecionado pega o seu asset correspondente
    for actor in selectedActors:
        if actor.__class__ ==  unreal.StaticMeshActor:
            components = actor.get_components_by_class(unreal.StaticMeshComponent)
            for component in components:
                componentName = systemLib.get_display_name(component).split(' ')[1]
                componentAsset = dictAssetsNames[componentName]
                # Caso tenha um componentAsset com o nome correspondente pegar as informações do mesmo 
                # e criar tags no Actor com base neles
                if componentAsset is not None:
                    tagValues = assetLibrary.get_metadata_tag_values(componentAsset)
                    tarefa = tagValues.get('FBX.Element_AY_Tarefa')
                    ordem = tagValues.get('FBX.Element_AY_OrdemNaTarefa')
                    quantidade = tagValues.get('FBX.Element_AY_QuantidadeNaTarefa')

                    # Cria as tags no Actor com base no elemento na metadata do asset
                    # Também checa se já existe uma tag no elemento que inicia com o mesmo prefixo
                    actorTags = actor.tags
                    actorTagsString = []
                    for tag in actorTags:
                        actorTagsString.append(str(tag))
                    
                    CriarTag(prefixTarefa, tarefa, actorTagsString, actorTags)
                    CriarTag(prefixOrdem, ordem, actorTagsString, actorTags)
                    CriarTag(prefixQuantidade, quantidade, actorTagsString, actorTags)
        else:
            print('Ator selecionado não é um StaticMeshActor')

def CriarTagComBaseNaMetadataDataTable():

    print('CriarTagComBaseNaMetadataDataTable')

    # Pega os atores selectionados
    actorSubSystem = unreal.get_editor_subsystem(actorUtils)
    selectedActors = actorSubSystem.get_selected_level_actors()

    # Pega todos os elementos que contém a chave Element_AY_Tarefa na sua metadata
    AdicionarTagPorMetadata('Element_AY_Tarefa', prefixTarefa)
    AdicionarTagPorMetadata('Element_AY_QuantidadeNaTarefa', prefixQuantidade)
    AdicionarTagPorMetadata('Element_AY_OrdemNaTarefa', prefixOrdem)

def LimparTagsAY():

    print('LimparTagsAY')

    # Pega os atores selectionados
    actorSubSystem = unreal.get_editor_subsystem(actorUtils)
    selectedActors = actorSubSystem.get_selected_level_actors()

    # Para cada ator selecionado pegar as suas tags
    for actor in selectedActors:
        actorTags = actor.tags
        print(len(actorTags))
        for tag in reversed(actorTags):
            if str(tag).startswith(prefixTarefa):
                actorTags.remove(tag)
            if str(tag).startswith(prefixOrdem):
                actorTags.remove(tag)
            if str(tag).startswith(prefixQuantidade):
                actorTags.remove(tag)
            
def CriarLevelSequenceTracks(dataTable):
    
    print('CriarLevelSequenceTracks')

    # Pega os atores selectionados
    actorSubSystem = unreal.get_editor_subsystem(actorUtils)
    selectedActors = actorSubSystem.get_selected_level_actors()

    # Verifica se o elemento selecionado é uma sequence
    if selectedActors[0].__class__ ==  unreal.LevelSequenceActor:

        # Cast o primeiro ator selecionado como LevelSequenceActor
        lsActor = unreal.LevelSequenceActor.cast(selectedActors[0])

        # Pega a LevelSequence que esta aberta
        levelSequence = unreal.LevelSequenceEditorBlueprintLibrary.get_current_level_sequence()

        # Pega a MovieSequence da LevelSequence
        movieSequence = lsActor.get_sequence()

        # Pega todos os atores com a tag
        actorsWithTag = unreal.GameplayStatics.get_all_actors_of_class_with_tag(lsActor, unreal.StaticMeshActor, 'AYTF_FundacaoProfunda')
        
        bindings = unreal.MovieSceneSequence.get_bindings(levelSequence)

        trackPadraomaterial = []

        # Duplica a track
        for bind in bindings:
            tracks = bind.get_tracks()
            for track in tracks:
                if track.get_display_name() == 'TrackMaterialPadrao'
                trackPadraomaterial.append(track)
                sections = track.get_sections()

        for actor in actorsWithTag:
            bindings.append(trackPadraomaterial[0])

        # for bind in bindings:
        #     tracks = bind.get_tracks()
        #     for track in tracks:
        #         print(track.get_display_name())
        #         sections = track.get_sections()
        #         for section in sections:
        #             print(section)
        #             channels = section.get_all_channels()
        #             for channel in channels:
        #                 print(channel)


        # # Adiciona uma track com binding para os atores
        # firstBind = levelSequence.add_possessable(actorsWithTag[0])
        # materialTrack = firstBind.add_track(unreal.MovieSceneComponentMaterialTrack)
        # newSection = materialTrack.add_section()
        # newSection.set_range(100,200)
        # channel = newSection.get_channels()[0]
        # channel.add
        # unreal.MovieSceneScriptingFloatChannel.add_key(channel, 10,0,0,unreal.SequenceTimeUnit.DISPLAY_RATE, unreal.MovieSceneKeyInterpolation.AUTO)
        # #MovieSceneScriptingFloatChannel
        
        

        for bind in bindings:
            tracks = bind.get_tracks()
            for track in tracks:
                print(track)
                sections = track.get_sections()
                for section in sections:
                    print(section)
                    channels = section.get_all_channels()
                    for channel in channels:
                        print(channel)
                    



                
            # print(bind)



        

        # Pega as MasterTracks da sequence e limpa as mesmas
        
        # masterTracks = unreal.MovieSceneSequence.get_master_tracks(movieSequence)
        # bindings = unreal.MovieSceneSequence.get_bindings(movieSequence)
        # masterTracksnames = []
        
        # for bind in bindings:
        #     print(bind.get_display_name())

        # for masterTrack in masterTracks:
        #     # unreal.MovieSceneSequence.remove_master_track(movieSequence, masterTrack)
        #     trackName = masterTrack.get_display_name()
        #     print(trackName)
        #     # masterTracksnames.append(trackName)        
        
        # Pega os nomes das linhas da DataTable
        # dtRowNames = dataTableLibrary.get_data_table_row_names(dataTable)

        # Para cada nome de linha criar uma track na sequence
        # for rowName in dtRowNames:
        #     newTrack = movieSequence.add_master_track(unreal.MovieSc)
        #     unreal.MovieSceneTrackExtensions.set_display_name(newTrack, rowName) # Define o nome da track
            



        # any(s for s in actorTagsString if s.startswith(prefixo)):


        
        #    print(rowName)
        #     print(unreal.DataTableRowHandle(dataTable, rowName))
        
    else:
        print('Não é um LevelSequenceActor, selecione um LevelSequenceActor no Level')



# endregion

# region SUBFUNÇÕES

def AdicionarTagPorMetadata(chave, prefixo):

    actorsValores = dataSmithLibrary.get_all_objects_and_values_for_key(chave, unreal.Actor)

    if len(actorsValores[0]) > 0 :

        actors = actorsValores[0]
        valores = actorsValores[1]

        #Para cada ator com a tarefa pegar suas tags e alterar o valor
        for i in range(len(actors)):
            actor = actors[i]
            actorTags = actor.tags
            actorTagsString = []
            for tag in actorTags:
                actorTagsString.append(str(tag))
            
            if any(s for s in actorTagsString if s.startswith(prefixo)):
                tagIndex = actorTagsString.index([s for s in actorTagsString if s.startswith(prefixo)][0])
                actorTags[tagIndex] = (prefixo + valores[i])
            else:
                actorTags.append(prefixo + valores[i])

def CriarTag(prefixo, tag, tagStrings, tags):
    if tag is not None:
        if any(s for s in tagStrings if s.startswith(prefixo)):
            index = tagStrings.index([s for s in tagStrings if s.startswith(prefixo)][0])
            tags[index] = (prefixo + tag)
        else:
            tags.append(prefixo + tag)

def DeletarTag(prefixo, tagStrings, tags):
    if any(s for s in tagStrings if s.startswith(prefixo)):
        index = tagStrings.index([s for s in tagStrings if s.startswith(prefixo)][0])
        unreal.Array.pop(tags, index)

# endregion

print('----- MEU CÓDIGO INICIA AQUI -----')

print('----- MEU CÓDIGO TERMINA AQUI -----')
