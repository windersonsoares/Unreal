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
            
def CriarLevelSequenceTracksB(dataTable):
    
    print('CriarLevelSequenceTracks')

    # Pega os nomes das linhas da DataTable
    dtRowNames = dataTableLibrary.get_data_table_row_names(dataTable)

    # Para cada nome de linha criar uma track na sequence
    for rowName in dtRowNames:
        print(rowName)

    # Pega os atores selectionados
    actorSubSystem = unreal.get_editor_subsystem(actorUtils)
    selectedActors = actorSubSystem.get_selected_level_actors()

    # Verifica se o elemento selecionado é uma sequence
    if selectedActors[0].__class__ ==  unreal.LevelSequenceActor:

        # Cast o primeiro ator selecionado como LevelSequenceActor
        lsActor = unreal.LevelSequenceActor.cast(selectedActors[0])

        # Pega a LevelSequence que esta aberta
        levelSequence = unreal.LevelSequenceEditorBlueprintLibrary.get_current_level_sequence()

        # Pega todos os atores com a tag
        actorsWithTag = unreal.GameplayStatics.get_all_actors_of_class_with_tag(lsActor, unreal.StaticMeshActor, 'AYTF_FundacaoProfunda')
        print('Existem ' + str(len(actorsWithTag)) + ' Atores com a TAG')

        # Cria um Array com o primeiro ator
        firstActorArray = [actorsWithTag[0]]

        # Pega o LevelSequenceEditorSubSystem
        editorSubsystem = unreal.get_editor_subsystem(unreal.LevelSequenceEditorSubsystem)

        bindings = unreal.MovieSceneSequence.get_bindings(levelSequence)

        for bind in bindings:
            tracks = bind.get_tracks()
            for track in tracks:
                print(track)
                sections = track.get_sections()
                for section in sections:
                    print(section)
                    channelsParameter = section.get_all_channels()
                    for channel in channelsParameter:
                        print(channel)

        
        # Adiciona o primeiro ator a Sequence
        #actorTrack = editorSubsystem.add_actors(firstActorArray)

        # Adiciona o primeiro componente do ator como uma track
        actorComponent = firstActorArray[0].get_component_by_class(unreal.StaticMeshComponent)
        componentBinding = levelSequence.add_possessable(actorComponent)

        # Adiciona uma track para alterar o valor do material do component
        materialValueTrack = componentBinding.add_track(unreal.MovieSceneComponentMaterialTrack)

        # Adiciona uma track para alterar o material do component
        materialChangeTrack = componentBinding.add_track(unreal.MovieScenePrimitiveMaterialTrack)

        # Adiciona uma track para alterar a visibilidade do ator
        visibilityTrack = componentBinding.get_parent().add_track(unreal.MovieSceneVisibilityTrack)

        # Adiciona uma seção com propriedade as tracks
        newSectionValue = materialValueTrack.add_section()
        newSectionMaterial = materialChangeTrack.add_section()
        newSectionVisibility = visibilityTrack.add_section()

        # Cast as seçãos criadas para seus tipos corretos
        parameterSection = unreal.MovieSceneParameterSection.cast(newSectionValue)
        materialChangeSection = unreal.MovieScenePrimitiveMaterialSection.cast(newSectionMaterial)
        visibilitySection = unreal.MovieSceneBoolSection.cast(newSectionVisibility)

        # Refresh na Sequence para mostrar as alterações
        unreal.LevelSequenceEditorBlueprintLibrary.refresh_current_level_sequence()

        # Adiciona uma chave de parâmetro escalar e define seu valor
        inicio = 100
        fim = 200
        inicioFrame = unreal.FrameNumber(inicio)
        fimFrame = unreal.FrameNumber(fim)
        antesDoInicioFrame = unreal.FrameNumber(inicio-1)
        aposOFimFrame = unreal.FrameNumber(fim+1)

        # Adiciona uma chave para criar automaticamente um channel e poder adicionar as chaves corretamente depois
        parameterSection.add_scalar_parameter_key("Curve", unreal.FrameNumber(0), 0.0)

        # Pega todos os channels da seção
        channelsParameter = parameterSection.get_all_channels()
        channelsMaterial = materialChangeSection.get_all_channels()
        channelsVisibility = visibilitySection.get_all_channels()

        # Cast o channel
        floatChannel = unreal.MovieSceneScriptingFloatChannel.cast(channelsParameter[0])
        materialChannel = unreal.MovieSceneScriptingObjectPathChannel.cast(channelsMaterial[0])
        boolChannel = unreal.MovieSceneScriptingBoolChannel.cast(channelsVisibility[0])

        # Pega os materiais
        materialObjeto = unreal.load_object(name = '/Game/Materials/M_CorBranca', outer = None)
        print(materialObjeto)
        materialEfeito = unreal.load_object(name = '/Game/Materials/MS_SimpleGlow_Inst', outer = None)
        print(materialEfeito)

        # Adiciona as chaves corretamente
        floatChannel.add_key(inicioFrame, 0.0,0,unreal.SequenceTimeUnit.DISPLAY_RATE)
        floatChannel.add_key(fimFrame, 2.0,0,unreal.SequenceTimeUnit.DISPLAY_RATE)

        #materialChannel.add_key(antesDoInicioFrame,materialObjeto,0,unreal.SequenceTimeUnit.DISPLAY_RATE)
        materialChannel.add_key(antesDoInicioFrame,materialEfeito,0,unreal.SequenceTimeUnit.DISPLAY_RATE)
        materialChannel.add_key(fimFrame,materialEfeito,0,unreal.SequenceTimeUnit.DISPLAY_RATE)
        materialChannel.add_key(aposOFimFrame,materialObjeto,0,unreal.SequenceTimeUnit.DISPLAY_RATE)

        boolChannel.add_key(antesDoInicioFrame, False, 0, unreal.SequenceTimeUnit.DISPLAY_RATE)
        boolChannel.add_key(inicioFrame, True, 0, unreal.SequenceTimeUnit.DISPLAY_RATE)

        # Remove a chave padrão
        chavePadrao = floatChannel.get_keys()[0]
        floatChannel.remove_key(chavePadrao)

        # Define o range da seção
        newSectionValue.set_start_frame_bounded(True)
        newSectionValue.set_end_frame_bounded(True)

        # Adiciona todos os atores com a mesma TAG a track
        editorSubsystem.add_actors_to_binding(actorsWithTag, componentBinding.get_parent())



        #unreal.LevelSequenceEditorBlueprintLibrary.refresh_current_level_sequence()


        # newSection.add
        # floatTrack = componentBinding.add_track(unreal.MovieSceneMaterialParameterSection)

        #componentBinding.set_parent(actorsWithTag[0])

        # # Adiciona todos os atores com a mesma TAG a track
        # editorSubsystem.add_actors_to_binding(actorsWithTag, actorTrack[0])

        # # Adiciona uma track para alterar o material do component
        # materialTrack = actorTrack[0].add_track(unreal.MovieSceneComponentMaterialTrack)

        # # Adiciona uma seção a track de material
        # 
        # newSection.
        # section.set_compo

        # Define o componente da seção


        # # Define o range da seção
        # newSection.set_range(100,200)

        # # Pega os canais da seção
        # channels = newSection.get_channels()

        # # # Adiciona um novo canal a seção
        # channels.

        # 
        # channel = newSection.get_channels()[0]






        
        
        # bindings = unreal.MovieSceneSequence.get_bindings(levelSequence)

        # print('Quantidade de BINDINGS: ' + str(len(bindings)))

        # trackPadraomaterial = []

        # # Duplica a track
        # for bind in bindings:
        #     if bind.get_display_name() == 'TrackMaterialPadrao':
        #         print('Encontrou a track TrackMaterialPadrao')
        #         trackPadraomaterial.append(bind)
        #     # for track in tracks:
        #     #     print(track)
        #         # if track.get_display_name() == 'TrackMaterialPadrao':
        #         #     trackPadraomaterial.append(track)
        #         #     print('Encontrou a track TrackMaterialPadrao')
        #         #     sections = track.get_sections()

        # actorTrack = print(levelSequenceSubSystem)

        # for actor in actorsWithTag:
            
        #     copiedTrack = unreal.LevelSequenceEditorSubsystem.copy_tracks(trackPadraomaterial)
        #     print(copiedTrack)


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
        
        

        # for bind in bindings:
        #     tracks = bind.get_tracks()
        #     for track in tracks:
        #         print(track)
        #         sections = track.get_sections()
        #         for section in sections:
        #             print(section)
        #             channels = section.get_all_channels()
        #             for channel in channels:
        #                 print(channel)
                    



                
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

def CriarLevelSequenceTracks(dataTable, dataInicial, dataFinal):

    # Pega a LevelSequence que esta aberta
    levelSequence = unreal.LevelSequenceEditorBlueprintLibrary.get_current_level_sequence()

    # Pega os atores selectionados
    actorSubSystem = unreal.get_editor_subsystem(actorUtils)
    selectedActors = actorSubSystem.get_selected_level_actors()

    # Calcula o tempo base da sequence
    tempoTotalSequence = levelSequence.get_playback_end_seconds()
    diasTotais = CalcularDiasTotais(dataInicial, dataFinal)
    print('Dias totais: ' + str(diasTotais))
    sequenceFrameRate = levelSequence.get_display_rate()

    # Pega o LevelSequenceEditorSubSystem
    editorSubsystem = unreal.get_editor_subsystem(unreal.LevelSequenceEditorSubsystem)

    # Pega as colunas da DataTable
    dataTableColumns = PegarDadosDataTableCronograma(dataTable)

    print(dataTableColumns)
    print(dataTableColumns[0])

    # Caso tenham colunas
    if len(dataTableColumns) > 0:
        # Para cada coluna
        for i in range(len(dataTableColumns[0])):
            
            tarefa = prefixTarefa + str(dataTableColumns[0][i]) # Nome da tarefa
            dataInicialTarefa = unreal.MathLibrary.date_time_from_string(dataTableColumns[1][i])
            dataFinalTarefa = unreal.MathLibrary.date_time_from_string(dataTableColumns[2][i])

            tempoInicialDaTarefa = CalcularTempoInicialDaTarefa(tempoTotalSequence, diasTotais, dataInicial, dataInicialTarefa)
            tempoFinalTarefa = CalcularTempoFinalDaTarefa(tempoTotalSequence, diasTotais, dataInicial, dataFinalTarefa)

            print('Tarefa: ' + tarefa + 'Tempo inicial: ' + str(tempoInicialDaTarefa) + 'Tempo final: ' + str(tempoFinalTarefa))

            # Pega todos os atores com a tag
            actorsWithTag = unreal.GameplayStatics.get_all_actors_of_class_with_tag(selectedActors[0], unreal.StaticMeshActor, tarefa)
            print('Existem ' + str(len(actorsWithTag)) + ' Atores com a TAG ' + str(tarefa))

            # Cria um Array com o primeiro ator caso existam atores com a tag
            if len(actorsWithTag) > 0:

                # Cria um Array com o primeiro ator
                firstActorArray = [actorsWithTag[0]]

                # Calcula os tempos em FRAMES
                inicio = unreal.MathLibrary.round(tempoInicialDaTarefa*sequenceFrameRate.numerator)
                fim = unreal.MathLibrary.round(tempoFinalTarefa*sequenceFrameRate.numerator)
                inicioFrame = unreal.FrameNumber(inicio)
                fimFrame = unreal.FrameNumber(fim)
                antesDoInicioFrame = unreal.FrameNumber(inicio-1)
                aposOFimFrame = unreal.FrameNumber(fim+1)

                # Pega o LevelSequenceEditorSubSystem
                editorSubsystem = unreal.get_editor_subsystem(unreal.LevelSequenceEditorSubsystem)
                
                # Adiciona o primeiro ator a Sequence
                #actorTrack = editorSubsystem.add_actors(firstActorArray)

                # Adiciona o primeiro componente do ator como uma track
                actorComponent = firstActorArray[0].get_component_by_class(unreal.StaticMeshComponent)
                componentBinding = levelSequence.add_possessable(actorComponent)

                # Adiciona uma track para alterar o valor do material do component
                materialValueTrack = componentBinding.add_track(unreal.MovieSceneComponentMaterialTrack)

                # Adiciona uma track para alterar o material do component
                materialChangeTrack = componentBinding.add_track(unreal.MovieScenePrimitiveMaterialTrack)

                # Adiciona uma track para alterar a visibilidade do ator
                visibilityTrack = componentBinding.get_parent().add_track(unreal.MovieSceneVisibilityTrack)

                # Adiciona uma seção com propriedade as tracks
                newSectionValue = materialValueTrack.add_section()
                newSectionMaterial = materialChangeTrack.add_section()
                newSectionVisibility = visibilityTrack.add_section()

                # Cast as seçãos criadas para seus tipos corretos
                parameterSection = unreal.MovieSceneParameterSection.cast(newSectionValue)
                materialChangeSection = unreal.MovieScenePrimitiveMaterialSection.cast(newSectionMaterial)
                visibilitySection = unreal.MovieSceneBoolSection.cast(newSectionVisibility)

                # Refresh na Sequence para mostrar as alterações
                unreal.LevelSequenceEditorBlueprintLibrary.refresh_current_level_sequence()

                # Adiciona uma chave para criar automaticamente um channel e poder adicionar as chaves corretamente depois
                parameterSection.add_scalar_parameter_key("Curve", unreal.FrameNumber(0), 0.0)

                # Pega todos os channels da seção
                channelsParameter = parameterSection.get_all_channels()
                channelsMaterial = materialChangeSection.get_all_channels()
                channelsVisibility = visibilitySection.get_all_channels()

                # Cast o channel
                floatChannel = unreal.MovieSceneScriptingFloatChannel.cast(channelsParameter[0])
                materialChannel = unreal.MovieSceneScriptingObjectPathChannel.cast(channelsMaterial[0])
                boolChannel = unreal.MovieSceneScriptingBoolChannel.cast(channelsVisibility[0])

                # Pega os materiais
                #materialObjeto = unreal.load_object(name = '/Game/Materials/M_CorBranca', outer = None)
                materialObjeto = unreal.StaticMeshComponent.cast(actorComponent).get_material(0)
                #materialEfeito = unreal.load_object(name = '/Game/Materials/MS_SimpleGlow_Inst', outer = None)
                materialEfeito = unreal.load_object(name = dataTableColumns[3][i], outer = None)

                # Adiciona as chaves corretamente
                floatChannel.add_key(inicioFrame, 0.0,0,unreal.SequenceTimeUnit.DISPLAY_RATE)
                floatChannel.add_key(fimFrame, 2.0,0,unreal.SequenceTimeUnit.DISPLAY_RATE)

                #materialChannel.add_key(antesDoInicioFrame,materialObjeto,0,unreal.SequenceTimeUnit.DISPLAY_RATE)
                materialChannel.add_key(antesDoInicioFrame,materialEfeito,0,unreal.SequenceTimeUnit.DISPLAY_RATE)
                materialChannel.add_key(fimFrame,materialEfeito,0,unreal.SequenceTimeUnit.DISPLAY_RATE)
                materialChannel.add_key(aposOFimFrame,materialObjeto,0,unreal.SequenceTimeUnit.DISPLAY_RATE)

                boolChannel.add_key(antesDoInicioFrame, False, 0, unreal.SequenceTimeUnit.DISPLAY_RATE)
                boolChannel.add_key(inicioFrame, True, 0, unreal.SequenceTimeUnit.DISPLAY_RATE)

                # Remove a chave padrão
                chavePadrao = floatChannel.get_keys()[0]
                floatChannel.remove_key(chavePadrao)

                # Define o range da seção
                newSectionValue.set_start_frame_bounded(True)
                newSectionValue.set_end_frame_bounded(True)

                # Adiciona todos os atores com a mesma TAG a track
                editorSubsystem.add_actors_to_binding(actorsWithTag, componentBinding.get_parent())

                # Renomeia a track
                componentBinding.get_parent().set_display_name(str(dataTableColumns[0][i]))
    else:
        print('Nenhum dado encontrado na DataTable')


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

def PegarDadosDataTableCronograma(dataTable):

    print('PegarDadosDataTableCronograma')

    # Estrutura da DataTable
    #structure = unreal.load_object(name = '/Game/Timeline/STR_CronogramaStruct.STR_CronogramaStruct', outer = None)

    # Pega os nomes das linhas da DataTable
    dtRowNames = unreal.DataTableFunctionLibrary.get_data_table_row_names(dataTable)

    # Colunas da DataTable
    dataTableColumns = []
    columnInicio = unreal.DataTableFunctionLibrary.get_data_table_column_as_string(dataTable, 'Inicio')
    columnTermino = unreal.DataTableFunctionLibrary.get_data_table_column_as_string(dataTable, 'Termino')
    columnMaterialEfeito = unreal.DataTableFunctionLibrary.get_data_table_column_as_string(dataTable, 'MaterialEfeito')

    dataTableColumns.append(dtRowNames)
    dataTableColumns.append(columnInicio)
    dataTableColumns.append(columnTermino)
    dataTableColumns.append(columnMaterialEfeito)

    return dataTableColumns

def CalcularDiasTotais(dataInicial, dataFinal):

    dataInicial = unreal.DateTime.cast(dataInicial)
    dataFinal = unreal.DateTime.cast(dataFinal)

    diasTotais = unreal.MathLibrary.get_days(unreal.MathLibrary.subtract_date_time_date_time(dataFinal, dataInicial))

    return(diasTotais)
   
def CalcularTempoInicialDaTarefa(tempoDaSequence, diasTotais, dataInicial, dataInicialTarefa):

    dataInicial = unreal.DateTime.cast(dataInicial)
    dataInicialTarefa = unreal.DateTime.cast(dataInicialTarefa)

    diasAteIniciarATarefa = unreal.MathLibrary.get_days(unreal.MathLibrary.subtract_date_time_date_time(dataInicialTarefa, dataInicial))

    print(diasAteIniciarATarefa)

    tempoInicial = (diasAteIniciarATarefa / diasTotais) * tempoDaSequence

    return tempoInicial

def CalcularTempoFinalDaTarefa(tempoDaSequence, diasTotais, dataInicial, dataFinalTarefa):

    dataInicial = unreal.DateTime.cast(dataInicial)
    dataFinalTarefa = unreal.DateTime.cast(dataFinalTarefa)

    diasAteFinalizarATarefa = unreal.MathLibrary.get_days(unreal.MathLibrary.subtract_date_time_date_time(dataFinalTarefa, dataInicial))

    print(diasAteFinalizarATarefa)

    tempoFinal = (diasAteFinalizarATarefa / diasTotais) * tempoDaSequence

    return tempoFinal



# endregion

print('----- MEU CÓDIGO INICIA AQUI -----')

print('----- MEU CÓDIGO TERMINA AQUI -----')
